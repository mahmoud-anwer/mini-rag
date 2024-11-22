import logging
from fastapi import APIRouter, Depends, UploadFile, status, Request
from fastapi.responses import JSONResponse
import aiofiles
from helpers.config import get_settings, Settings
from controllers import DataController, ProcessController
from models import ResponseSignal, DataChunk
from services.ProjectModel import ProjectModel
from services.ChunkModel import ChunkModel
from .schemes.data import ProcessRequest
from minio import Minio
from minio.error import S3Error
from io import BytesIO


# Create a logger to log events and errors
logger = logging.getLogger('my_logger')
logger.setLevel(logging.DEBUG)  # Set the minimum log level to DEBUG for detailed logs

# Create a file handler to write logs to a file
file_handler = logging.FileHandler('uvicorn.log')
file_handler.setLevel(logging.DEBUG)  # Set file log level to DEBUG

# Create a log format to structure the logs
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Creating an APIRouter instance with a prefix and tags for the API endpoints
data_router = APIRouter(prefix="/api/v1/data", tags=["api_v1_data"])


@data_router.post("/upload/{project_id}")
async def upload_data(
    request: Request,
    project_id: str,
    file: UploadFile,
    app_settings: Settings = Depends(get_settings)
):
    """
    Endpoint to upload data for a specific project.

    This endpoint handles file upload, validates its type and size, and saves it
    to the specified project directory. Returns an error if the file is invalid.

    Args:
        project_id (str): The ID of the project to which the file belongs.
        file (UploadFile): The file to be uploaded.
        app_settings (Settings): Application settings dependency injection.

    Returns:
        JSONResponse: Response indicating success or failure of the upload operation.
    """

    # Retrieve the project model to interact with the project data
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    # Initialize the DataController to handle file validation
    data_controller = DataController()
    # Validate the uploaded file type and size
    is_valid, signal = data_controller.validate_uploaded_file(file=file)

    if not is_valid:
        # If file is invalid, return a Bad Request response
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content={"signal": signal}
        )

    # Generate a unique file path and ID for saving the file
    # file_path, file_id = data_controller.generate_unique_filepath(
    file_id = data_controller.generate_unique_fileid(
        orig_file_name=file.filename,
        project_id=project_id
    )

    # Configure the MinIO client
    minio_client = Minio(
        app_settings.MINIO_URL,
        access_key=app_settings.MINIO_ACCESS_KEY,
        secret_key=app_settings.MINIO_SECRET_KEY,
        secure=True,  # Set to True if using HTTPS
    )

    # Specify the bucket name and file details
    bucket_name = app_settings.MINIO_BUCKET_NAME

    # Ensure the bucket exists
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")
    except S3Error as err:
        logger.error("Error checking bucket: %s", err)
        print(f"Error checking bucket: {err}")

    # Upload file to MinIO
    try:
        # Save to the project id
        complete_file_id=f"{project_id}/{file_id}"

        # Read file content as a stream
        file_content = await file.read()

        minio_client.put_object(
            bucket_name,
            complete_file_id,  # Save with the original file name
            data=BytesIO(file_content),  # File content as stream
            length=len(file_content),  # Size of the file
            content_type=file.content_type,  # File MIME type
        )
        print(f"'{file.filename}' uploaded to bucket '{bucket_name}' as '{file_id}'.")
        # Return a success response with file ID and project ID
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "signal": ResponseSignal.FILE_UPLOADED_SUCCESS.value,
                "file_id": file_id,
                "project_id": str(project.id)
            },
        )
    except S3Error as err:
        logger.error("Error while uploading file: %s", err)
        print(f"Error uploading file: {err}")

        # Return a failed upload response
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.FILE_UPLOADED_FAILED.value},
        )


@data_router.post("/process/{project_id}")
async def process_endpoint(request: Request,
                           project_id: str,
                           process_request: ProcessRequest,
                           app_settings: Settings = Depends(get_settings)): # pylint: disable=too-many-locals
    """
    Endpoint to process a file for a specific project.

    This endpoint processes the file content by dividing it into chunks, overlapping [optional].
    If processing fails, a 400 Bad Request response is returned.

    Args:
        project_id (str): The ID of the project for processing the file.
        process_request (ProcessRequest): The request body containing file ID,
                                          chunk size, overlap size, and reset flag.

    Returns:
        JSONResponse: A response indicating success or failure of the processing operation.
        list: A list of processed file chunks if successful.
    """

    # Extract the parameters for processing from the request body
    file_id = process_request.file_id
    chunk_size = process_request.chunk_size
    overlap_size = process_request.overlap_size
    do_reset = process_request.do_reset

    # Retrieve the project model and fetch the project by project_id
    project_model = ProjectModel(db_client=request.app.db_client)
    project = await project_model.get_project_or_create_one(project_id=project_id)

    # Initialize the process controller to handle file processing logic
    process_controller = ProcessController(project_id=project_id)

    file_content = process_controller.get_file_content(project_id=project_id, file_id=file_id)

    # Process the file content into chunks
    file_chunks = process_controller.process_file_content(
        file_content=file_content,
        file_id=file_id,
        chunk_size=chunk_size,
        overlap_size=overlap_size
    )

    # Check if file chunks are successfully processed
    if file_chunks is None or len(file_chunks) == 0:
        # Return a failure response if no chunks were processed
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"signal": ResponseSignal.PROCESSING_FAILD.value}
        )

    # Prepare the file chunks to be saved in the database
    file_chunks_records = [
        DataChunk(
            chunk_text=chunk.page_content,
            chunk_metadata=chunk.metadata,
            chunk_order=i+1,
            chunk_project_id=project.id,
        )
        for i, chunk in enumerate(file_chunks)
    ]

    # Initialize the ChunkModel to interact with chunk data
    chunk_model = ChunkModel(db_client=request.app.db_client)

    if do_reset == 1:
        # If reset flag is set, delete existing chunks for the project
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
