import os
from io import BytesIO
from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error
from .BaseController import BaseController


class MinIOController(BaseController):
    """
    Controller for handling interactions with MinIO, including file uploads and downloads.
    Inherits from BaseController to access shared application settings.
    """

    def __init__(self):
        """
        Initialize the MinIOController with a MinIO client and bucket configuration.

        Attributes:
            minio_client (Minio): Client for interacting with the MinIO server.
            bucket_name (str): Name of the bucket used for storage operations.
        """
        super().__init__()  # Initialize the BaseController
        self.minio_client = Minio(
            self.app_settings.MINIO_URL,  # URL for the MinIO server
            access_key=self.app_settings.MINIO_ACCESS_KEY,  # Access key for MinIO authentication
            secret_key=self.app_settings.MINIO_SECRET_KEY,  # Secret key for MinIO authentication
            secure=True  # Use HTTPS for secure communication
        )
        self.bucket_name = self.app_settings.MINIO_BUCKET_NAME  # Bucket name from settings

    async def upload_file(self, complete_file_id: str, file: UploadFile):
        """
        Upload a file to MinIO.

        Ensures the bucket exists and uploads the file to the bucket.

        Args:
            complete_file_id (str): Unique identifier (key) for the file in MinIO.
            file (UploadFile): The file to upload, received from FastAPI.

        Returns:
            bool: True if the upload was successful, False otherwise.
        """
        # Ensure the bucket exists or create it if necessary
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)  # Create bucket if it doesn't exist
                print(f"Bucket '{self.bucket_name}' created.")
            else:
                print(f"Bucket '{self.bucket_name}' already exists.")
        except S3Error as err:
            print(f"Error checking bucket: {err}")  # Log error for bucket existence
            return False

        # Upload the file content to MinIO
        try:
            file_content = await file.read()  # Read file content as bytes
            self.minio_client.put_object(
                self.bucket_name,
                complete_file_id,  # Key for saving the file in MinIO
                data=BytesIO(file_content),  # File content as a stream
                length=len(file_content),  # File size
                content_type=file.content_type  # File MIME type
            )
            print(f"'{file.filename}' uploaded to '{self.bucket_name}' as '{complete_file_id}'.")
            return True

        except S3Error as err:
            print(f"Error uploading file: {err}")  # Log error during upload
            return False

    def download_file(self, project_id: str, file_id: str):
        """
        Download a file from MinIO to a local path.

        Args:
            project_id (str): ID of the project associated with the file.
            file_id (str): Unique identifier of the file within the project.

        Returns:
            None: Downloads the file to a local directory.
        """
        # Construct paths and object name
        project_path = self.get_file_path(project_id=project_id)  # Get the local project path
        file_path = os.path.join(project_path, file_id)  # Full local path for the file
        object_name = f"{project_id}/{file_id}"  # Key of the file in the bucket

        # Ensure the bucket exists before downloading
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                print(f"Bucket '{self.bucket_name}' doesn't exist.")
                return False
        except S3Error as err:
            print(f"Error checking bucket: {err}")  # Log error for bucket existence check
            return False

        # Download the file from MinIO to the specified path
        try:
            self.minio_client.fget_object(
                self.bucket_name,  # Bucket name
                object_name,  # Key of the file in the bucket
                file_path  # Local path to save the file
            )
            print(f"File '{object_name}' downloaded to '{file_path}'.")
            return True
        except S3Error as err:
            print(f"Error downloading file: {err}")  # Log error during download
            return False
