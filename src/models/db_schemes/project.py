from typing import Optional
from pydantic import BaseModel, Field, field_validator
from bson.objectid import ObjectId
from pymongo import ASCENDING


class Project(BaseModel):
    """
    Data model for a project.

    Attributes:
        _id (Optional[ObjectId]): The unique identifier for the project in the database (nullable).
        project_id (str): The alphanumeric ID of the project [required, minimum length of 1].
    """

    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator('project_id')
    def validate_project_id(cls, value):    # pylint: disable=no-self-argument
        """
        Validates that the project_id is alphanumeric.

        Args:
            value (str): The project ID to validate.

        Returns:
            str: The validated project ID.

        Raises:
            ValueError: If the project_id is not alphanumeric.
        """
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value

    class Config:
        """
        Configuration for the Pydantic model.

        Attributes:
            arbitrary_types_allowed (bool): Enables the use of non-standard types like ObjectId.
        """
        arbitrary_types_allowed = True

    @classmethod
    def get_indices(cls):
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
                    ("project_id", ASCENDING)
                ],
                "name": "project_id_index_1",
                "unique": True
            }
        ]
