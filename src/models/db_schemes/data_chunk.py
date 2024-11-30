from typing import Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from pymongo import ASCENDING


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

    @classmethod
    def get_indexes(cls):
        """
        Returns a list of index specifications for the collection.

        This method defines the indexes to be created on the collection.
        Indexes are important for optimizing query performance, especially
        for fields that are frequently queried or sorted.

        In this case, we define an index on the "chunk_project_id" field,
        which is not unique, meaning multiple documents can have the same
        "chunk_project_id".

        Returns:
            list: A list of index definitions, each represented by a dictionary.
                  Each dictionary includes:
                  - 'key': The field(s) on which to create the index.
                  - 'name': The name of the index.
                  - 'unique': Whether the index enforces uniqueness (False in this case).
        """
        return [
            {
                "key": [
                    ("chunk_project_id", ASCENDING)  # Indexes "chunk_project_id" field in ascending order
                ],
                "name": "chunk_project_id_index_1",  # The name of the index
                "unique": False  # This index does not enforce uniqueness
            }
        ]
