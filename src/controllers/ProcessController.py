import os
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import FileExtensions
from .BaseController import BaseController
from .ProjectController import ProjectController


class ProcessController(BaseController):
    """
    Controller class for handling file processing operations.

    Inherits from BaseController to utilize common functionalities and integrates
    with ProjectController to manage project-specific file paths.
    """

    def __init__(self, project_id: str):
        """
        Initializes the ProcessController instance.

        Args:
            project_id (str): The ID of the project to be processed.
        """
        super().__init__()
        self.project_id = project_id
        self.project_path = ProjectController().get_file_path(project_id=project_id)

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

    def get_file_content(self, file_id: str):
        """
        Loads the content of the specified file using the appropriate loader.

        Args:
            file_id (str): The ID of the file.

        Returns:
            list: The content of the file.
        """
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
