import os
import re
from fastapi import UploadFile
from models import ResponseSignal
from .BaseController import BaseController
from .ProjectController import ProjectController


class DataController(BaseController):
    """
    Controller class for handling data-related operations.

    Inherits from BaseController to utilize common functionalities.
    """
    def __init__(self):
        """
        Initializes the DataController instance.

        Sets up the size scale for file size validation.
        """
        super().__init__()
        self.size_scale = 1048576

    def validate_uploaded_file(self, file: UploadFile):
        """
        Validates the uploaded file's type and size.

        Args:
            file (UploadFile): The uploaded file to validate.

        Returns:
            tuple: A tuple containing a boolean indicating validity and a response signal.
        """
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value

        return True, ResponseSignal.FILE_VALIDATED_SUCCESS

    def get_clean_file_name(self, orig_file_name: str) -> str:
        """
        Cleans the original file name by removing special characters and spaces.

        Args:
            orig_file_name (str): The original file name.

        Returns:
            str: The cleaned file name.
        """
        # strip():
        # to removes any leading and trailing whitespace characters from the orig_file_name string.
        # re.sub():
        # replaces all occurrences of the pattern in the input string with the given string.
        # '^\w.':
        # not a word charachter or dot
        cleaned_file_name = re.sub(r"[^\w.]", "", orig_file_name.strip())

        # Replace spaces with underscores
        cleaned_file_name = cleaned_file_name.replace(" ", "_")

        return cleaned_file_name

    def generate_unique_filepath(self, orig_file_name: str, project_id: str) -> tuple:
        """
        Generates a unique file path for the uploaded file within the project directory.

        Args:
            orig_file_name (str): The original file name.
            project_id (str): The ID of the project.

        Returns:
            tuple: A tuple containing the new file path and the unique file ID.
        """
        # Generate a random string to ensure uniqueness
        random_key = self.generate_random_string()
        project_path = ProjectController().get_file_path(project_id=project_id)

        # Clean the original file name
        cleaned_file_name = self.get_clean_file_name(orig_file_name=orig_file_name)

        # Create a unique file ID by combining the random key and cleaned file name
        file_id = random_key + "_" + cleaned_file_name
        new_file_path = os.path.join(project_path, file_id)

        # Ensure the file path is unique by checking if it already exists
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            file_id = random_key + "_" + cleaned_file_name
            new_file_path = os.path.join(project_path, file_id)

        return new_file_path, file_id
