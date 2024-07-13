import logging
from fastapi import APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
import aiofiles
from helpers.config import get_settings, Settings
from controllers import DataController, ProcessController
from models import ResponseSignal
from .schemes.data import ProcessRequest


# Create a logger
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Set the minimum log level for the logger

# Create a file handler
file_handler = logging.FileHandler('uvicorn.log')
file_handler.setLevel(logging.DEBUG)  # Set the minimum log level for the file handler

# Create a log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(file_handler)

# Creating an APIRouter instance with a prefix and tags
data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1_data"])


@data_router.post("/upload/{project_id}")
async def upload_data(
    project_id: str, file: UploadFile, app_settings: Settings = Depends(get_settings)
):
    """
    Endpoint to upload data for a specific project.

    This endpoint handles the uploading of a file, validating its type and size,
    and saving it to the specified project directory. If the file is invalid,
    a 400 Bad Request response is returned.

    Args:
        project_id (str): The ID of the project to which the file belongs.
        file (UploadFile): The file to be uploaded.
        app_settings (Settings): Application settings dependency injection.

    Returns:
        JSONResponse: A response indicating success or failure of the upload operation.
    """
    data_controller = DataController()
    # Validate the file type and size
    is_valid, signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"signal": signal}
        )

    # project_dir_path = ProjectController().get_file_path(project_id=project_id)
    file_path, file_id = data_controller.generate_unique_filepath(
        orig_file_name=file.filename, project_id=project_id
    )

    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:
        logger.error("Error while uploading file: %s", e)

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOADED_FAILED.value},
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
            "file_id": file_id,
        },
    )


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):
    """
    Endpoint to process a file for a specific project.

    This endpoint processes the content of a file by dividing it into chunks with
    optional overlapping. If the processing fails, a 400 Bad Request response is returned.

    Args:
        project_id (str): The ID of the project for which the file is being processed.
        process_request (ProcessRequest): The request body containing file ID, chunk size,
                                          overlap size, and reset flag.

    Returns:
        JSONResponse: A response indicating success or failure of the processing operation.
        list: A list of processed file chunks if the operation is successful.
    """
    # The below parameters I can send via body on the request
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size

    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)

    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size,
    )

    if file_chunks is None or len(file_chunks) == 0:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILD.value},
        )

    return file_chunks
