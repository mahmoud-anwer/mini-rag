from typing import Optional
from pydantic import BaseModel

class ProcessRequest(BaseModel):
    """
    Data model for process requests.

    Attributes:
        file_id (str): The ID of the file to be processed [required]
        chunk_size (Optional[int]): The size of chunks, default to 100
        overlap_size (Optional[int]): The size of overlap between chunks, default to 20
        do_reset (Optional[int]): Flag to indicate whether to reset the process, default to false
    """

    file_id: str
    chunk_size: Optional[int] = 100
    overlap_size: Optional[int] = 20
    do_reset: Optional[int] = 0
