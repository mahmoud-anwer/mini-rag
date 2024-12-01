from enum import Enum


class ResponseSignal(Enum):
    FILE_TYPE_NOT_SUPPORTED = "file type is not supported."
    FILE_SIZE_EXCEEDED = "file size is larger than expected."
    FILE_UPLOADED_FAILED = "file uploaded failed."
    FILE_UPLOADED_SUCCESS = "file uploaded successfully."
    FILE_DOWNLOADED_FAILED = "file downloaded failed."
    FILE_VALIDATED_SUCCESS = "file validated successfully."
    PROCESSING_FAILD = "processing failed."
    PROCESSING_SUCCESS = "processing succeeded."
    CHUNKS_DELETED = "chunks have been deleted."
    NO_FILES_ERROR = "files are not exist"
    FILE_ID_ERROR = "no file exist with this id."
