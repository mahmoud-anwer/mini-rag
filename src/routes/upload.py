from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers import get_settings, Settings
from models import ResponseSignal, Asset, AssetTypeEnum
from services import ProjectModel, AssetModel
from controllers import MinIOController, FileController
from utils.logger import logger


# Creating an APIRouter instance with a prefix "/api/v1/data" and tags for the API endpoints
upload_router = APIRouter(prefix="/api/v1/data", tags=["api_v1_data"])

# Endpoint to upload data for a specific project
@upload_router.post("/upload/{project_id}")
# pylint: disable=too-many-locals
async def upload_data(
    request: Request,  # FastAPI's Request object to handle HTTP requests
    project_id: str,   # Project ID to associate the uploaded file
    file: UploadFile,  # The file to be uploaded
    app_settings: Settings = Depends(get_settings)  # Dependency injection for app settings
):
    """
    Endpoint to upload data for a specific project.
    This endpoint handles file upload, validates its type and size,
    and saves it to the project directory.
    Returns an error if the file is invalid.
    """
    # Retrieve the project model to interact with project data from the database
    project_model = await ProjectModel.create_instance(db_client=request.app.db_client)

    # Retrieves an existing project by its ID or creates a new one if it doesn't exist.
    project = await project_model.get_project_or_create_one(project_id=project_id)

    # Create a FileController instance for the given project_id to manage file-related operations
    file_controller = FileController(project_id)

    # Validate the uploaded file's type and size
    is_valid, signal = file_controller.validate_uploaded_file(file=file)

    if not is_valid:
        # If the file is invalid, return a Bad Request response with the error signal
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": signal}
        )

    # Generate a unique file ID for the uploaded file
    file_id = file_controller.generate_unique_fileid(orig_file_name=file.filename)

    complete_file_id = f"{project_id}/{file_id}"

    # Create a MinIOController instance to manage file uploads to MinIO storage
    minio_controller = MinIOController()
    is_uploaded = await minio_controller.upload_file(complete_file_id, file)

    if is_uploaded:
        # If the file upload is successful, store assets into the database,
        # and return a successful response with the file ID and project ID
        logger.info("File: %s has been uploaded successfully.", file_id)

        asset_model = await AssetModel.create_instance(db_client=request.app.db_client)
        asset = Asset(asset_project_id=project.id,
                      asset_type=AssetTypeEnum.FILE.value,
                      asset_name=file_id,
                      asset_size=file.size)
        asset_record = await asset_model.create_asset(asset=asset)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                "file_id": asset_record.asset_name,
                "project_id": str(project.id)
            },
        )

    # If the file upload fails, return a Bad Request response with the failure signal
    return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOADED_FAILED.value},
    )
