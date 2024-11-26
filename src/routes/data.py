import logging
from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from models import ResponseSignal, DataChunk
from services.ProjectModel import ProjectModel
from services.ChunkModel import ChunkModel
from controllers.MinIOController import MinIOController
from controllers.FileController import FileController
from .schemes.data import ProcessRequest

# Create a logger to log events and errors
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Set the minimum log level to DEBUG for detailed logs

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('uvicorn.log')
file_handler.setLevel(logging.DEBUG)  # Set file log level to DEBUG

# Create a log format to structure the logs with timestamp, logger name, log level, and message
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger to enable logging to file
logger.addHandler(file_handler)

# Creating an APIRouter instance with a prefix "/api/v1/data" and tags for the API endpoints
data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1_data"])

# Endpoint to upload data for a specific project
@data_router.post("/upload/{project_id}")
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
    file_id = file_controller.generate_unique_fileid(
        orig_file_name=file.filename,
        project_id=project_id
    )

    complete_file_id = f"{project_id}/{file_id}"

    # Create a MinIOController instance to manage file uploads to MinIO storage
    minio_controller = MinIOController()
    is_uploaded = await minio_controller.upload_file(complete_file_id, file)

    if is_uploaded:
        # If the file upload is successful, return a successful response with the file ID and project ID
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                "file_id": file_id,
                "project_id": str(project.id)
            },
        )

    # If the file upload fails, return a Bad Request response with the failure signal
    return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOADED_FAILED.value},
    )


# Endpoint to process a file for a specific project
@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request,                                       # pylint: disable=too-many-locals
                           project_id: str,  # Project ID to associate the file processing
                           process_request: ProcessRequest,  # Request body containing processing details
                           app_settings: Settings = Depends(get_settings)):  # Dependency injection for app settings
    """
    Endpoint to process a file for a specific project.
    The file is divided into chunks, and optional overlap can be specified.
    If processing fails, a 400 Bad Request response is returned.
    """
    # Extract the parameters from the request body (ProcessRequest)
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    # Retrieve the project model to fetch the project data from the database
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    # Initialize the FileController to handle file processing
    file_controller = FileController(project_id)

    # Fetch the file content using the file controller
    file_content = file_controller.get_file_content(project_id=project_id, file_id=file_id)

    # Process the file content into chunks using the specified chunk size and overlap size
    file_chunks = file_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    # If no chunks were processed, return a failure response
    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILD.value}
        )

    # Prepare the processed file chunks to be saved into the database
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id,
        )
        for i, chunk in enumerate(file_chunks)
    ]

    # Initialize the ChunkModel to handle chunk data in the database
    chunk_model = ChunkModel(db_client=request.app.db_client)

    if do_reset == 1:
        # If the reset flag is set, delete existing chunks associated with the project
        deleted_chunks = await chunk_model.delete_chunks_by_project_id(project_id=project.id)
        return JSONResponse(
            content={
                "signal": ResponseSignal.CHUNKS_DELETED.value,
                "deleted_chunks": deleted_chunks
            }
        )

    # Insert the newly processed chunks into the database
    no_records = await chunk_model.insert_many_chunks(chunks=file_chunks_records)
    return JSONResponse(
        content={
            "signal": ResponseSignal.PROCESSING_SUCCESS.value,
            "inserted_chunks": no_records
        }
    )
