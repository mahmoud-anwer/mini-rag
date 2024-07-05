from pydantic import BaseModel
from typing import Optional


class ProcessRequest(BaseModel):
    """
    Data model for process requests.

    Attributes:
        file_id (str): The ID of the file to be processed [required].
        chunk_size (Optional[int]): The size of chunks, defaulting to 100 [optional].
        overlap_size (Optional[int]): The size of overlap between chunks, defaulting to 20 [optional].
        do_reset (Optional[int]): Flag to indicate whether to reset the process, defaulting to 0 (false) [optional].
    """

    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0
