import re
import time
import uuid
from fastapi import UploadFile
from models import ResponseSignal
from controllers.BaseController import BaseController


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

    def generate_unique_fileid(self, orig_file_name: str, project_id: str) -> tuple:
        """
        Generates a unique file path for the uploaded file within the project directory.

        Args:
            orig_file_name (str): The original file name.
            project_id (str): The ID of the project.

        Returns:
            tuple: A tuple containing the new file path and the unique file ID.
        """

        # Clean the original file name
        cleaned_file_name = self.get_clean_file_name(orig_file_name=orig_file_name)

        # Generate a UUID (UUIDv4)
        uuid4 = uuid.uuid4()

        # Add timestamp-based entropy
        timestamp_entropy = int(time.time() * 1000000)  # Microsecond precision timestamp

        # Create a unique file ID
        file_id = f"{uuid4}-{timestamp_entropy}-{cleaned_file_name}"

        return file_id
