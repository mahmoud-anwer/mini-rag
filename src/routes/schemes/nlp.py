from typing import Optional
from pydantic import BaseModel

class PushRequest(BaseModel):
    """
    Request model for pushing data into the vector database.

    Attributes:
        do_reset (Optional[int]): Flag indicating whether to reset the collection before pushing the data.
                                   Defaults to 0 (no reset).
    """
    do_reset: Optional[int] = 0

class SearchRequest(BaseModel):
    """
    Request model for searching the vector database.

    Attributes:
        text (str): The query text to search for in the vector database.
        limit (Optional[int]): The maximum number of search results to return. Defaults to 5.
    """
    text: str
    limit: Optional[int] = 5
