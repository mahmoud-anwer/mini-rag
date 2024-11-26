import re
import time
import uuid
import os
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from fastapi import UploadFile
from models import FileExtensions, ResponseSignal
from .MinIOController import MinIOController
from .BaseController import BaseController



class FileController(BaseController):
    def __init__(self, project_id: str):
        super().__init__()
        self.size_scale = 1048576
        self.project_id = project_id
        self.project_path = super().get_file_path(project_id=project_id)

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

    def get_file_extension(self, file_id: str) -> str:
        """
        Retrieves the file extension from the given file ID.

        Args:
            file_id (str): The ID of the file.

        Returns:
            str: The file extension.
        """
        return os.path.splitext(file_id)[-1]

    def get_file_loader(self, file_id: str):
        """
        Determines the appropriate file loader based on the file extension.

        Args:
            file_id (str): The ID of the file.

        Returns:
            FileLoader: An instance of the appropriate file loader or None if unsupported.
        """
        file_extension = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id)

        if file_extension == FileExtensions.TEXT.value:
            return TextLoader(file_path, encoding="utf-8")

        if file_extension == FileExtensions.PDF.value:
            return PyMuPDFLoader(file_path)

        return None
    def get_file_content(self,project_id: str, file_id: str):
        """
        Loads the content of the specified file using the appropriate loader.

        Args:
            file_id (str): The ID of the file.

        Returns:
            list: The content of the file.
        """
        minio_controller = MinIOController()
        minio_controller.download_file(project_id=project_id, file_id=file_id)



        loader = self.get_file_loader(file_id=file_id)
        return loader.load()

    def process_file_content(
        self,
        file_content: list,
        file_id: str,
        chunk_size: int = 100,
        overlap_size: int = 20,
    ) -> list:
        """
        Processes the file content by splitting it into chunks with optional overlap.

        Args:
            file_content (list): The content of the file.
            file_id (str): The ID of the file.
            chunk_size (int): The size of each chunk. Defaults to 100.
            overlap_size (int): The size of overlap between chunks. Defaults to 20.

        Returns:
            list: A list of processed file chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap_size,
            length_function=len,
        )

        file_content_texts = [rec.page_content for rec in file_content]

        file_content_metadata = [rec.metadata for rec in file_content]

        chunks = text_splitter.create_documents(
            file_content_texts, metadatas=file_content_metadata
        )

        return chunks
