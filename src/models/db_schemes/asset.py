from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from bson.objectid import ObjectId
from pymongo import ASCENDING


class Asset(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(ge=0, default=None)
    asset_config: dict = Field(default=None)
    asset_created_at: datetime = Field(default=datetime.utcnow)

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
        Class method to retrieve the indexes for the collection.

        This method returns a list of indexes that should be created for the 
        collection. Each index is represented by a dictionary containing:
            - 'key': The field(s) to index.
            - 'name': The name of the index.
            - 'unique': A boolean indicating whether the index should enforce uniqueness.

        Returns:
            list: A list of dictionaries where each dictionary defines an index 
                with the fields 'key', 'name', and 'unique'.
        """
        return [
            {
                "key": [
                    ("asset_project_id", ASCENDING)
                ],
                "name": "asset_project_id_index_1",
                "unique": False
            },
            {
                "key": [
                    ("asset_project_id", ASCENDING),
                    ("asset_name", ASCENDING)
                ],
                "name": "asset_project_id_name_index_1",
                "unique": True
            }
        ]
