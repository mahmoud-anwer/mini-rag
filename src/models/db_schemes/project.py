from typing import Optional
from pydantic import BaseModel, Field, validator
from bson.objectid import ObjectId

class Project(BaseModel):
    """
    Data model for a project.

    Attributes:
        _id (Optional[ObjectId]): The unique identifier for the project in the database (nullable).
        project_id (str): The alphanumeric ID of the project [required, minimum length of 1].
    """

    _id: Optional[ObjectId]
    project_id: str = Field(..., min_length=1)

    @validator('project_id')
    def validate_project_id(self, cls, value):
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
