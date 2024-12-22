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
    PROJECT_NOT_FOUND_ERROR = "project not found"
    INSERT_INTO_VECTORDB_ERROR = "insert into vectordb error"
    INSERT_INTO_VECTORDB_SUCCESS = "insert into vectordb success"
    VECTORDB_COLLECTION_RETRIEVED = "vectordb collection retrieved"
    VECTORDB_SEARCH_ERROR = "vectordb_search_error"
    VECTORDB_SEARCH_SUCCESS = "vectordb_search_success"
    RAG_ANSWER_ERROR = "rag_anwer_error"
    RAG_ANSWER_SUCCESS = "rag_anwer_success"
