from typing import Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    """
    Data model for a data chunk.

    Attributes:
        _id (Optional[ObjectId]): The unique identifier for the chunk in the database (nullable).
        chunk_text (str): The content of the chunk [required, minimum length of 1].
        chunk_metadata (dict): Metadata associated with the chunk [required].
        chunk_order (int): The order of the chunk in a sequence [required, must be greater than 0].
        chunk_project_id (ObjectId): The ID of the project this chunk belongs to [required].
    """

    id: Optional[ObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId

    class Config:
        """
        Configuration for the Pydantic model.

        Attributes:
            arbitrary_types_allowed (bool): Enables the use of non-standard types like ObjectId.
        """
        arbitrary_types_allowed = True
