from fastapi import APIRouter, Depends, status, Request
from fastapi.responses import JSONResponse
from helpers import get_settings, Settings
from models import ResponseSignal, DataChunk
from services import ProjectModel, ChunkModel
from controllers import FileController
from .schemes.data import ProcessRequest

process_router = APIRouter(prefix="/api/v1/data", tags=["api_v1_data"])

# Endpoint to process a file for a specific project
@process_router.post("/process/{project_id}")
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
    chunk_model = await ChunkModel.create_instance(db_client=request.app.db_client)

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
