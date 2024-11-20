from enum import Enum


class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file type is not supported."
    FILE_SIZE_EXCEEDED = "file size is larger than expected."
    FILE_UPLOADED_FAILED = "file uploaded failed."
    FILE_UPLOADED_SUCCESS = "file uploaded successfully."
    FILE_VALIDATED_SUCCESS = "file validated successfully."
    PROCESSING_FAILD = "file processing failed."
    PROCESSING_SUCCESS = "file processing succeeded."
    CHUNKS_DELETED = "chunks have been deleted."
