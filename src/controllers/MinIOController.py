import os
from io import BytesIO
from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error
from .BaseController import BaseController


class MinIOController(BaseController):
    def __init__(self):
        super().__init__()
        self.minio_client = Minio(
            self.app_settings.MINIO_URL,
            access_key=self.app_settings.MINIO_ACCESS_KEY,
            secret_key=self.app_settings.MINIO_SECRET_KEY,
            secure=True
        )
        self.bucket_name = self.app_settings.MINIO_BUCKET_NAME

    async def upload_file(self, complete_file_id: str, file: UploadFile):
        """
            TODO
        """
        # Ensure the bucket exists
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)
                print(f"Bucket '{self.bucket_name}' created.")
            else:
                print(f"Bucket '{self.bucket_name}' already exists.")
        except S3Error as err:
            print(f"Error checking bucket: {err}")

        # Upload file to MinIO
        try:
            # Save to the project id
            # complete_file_id=f"{project_id}/{file_id}"

            # Read file content as a stream
            file_content = await file.read()

            self.minio_client.put_object(
                self.bucket_name,
                complete_file_id,  # Save with the original file name
                data=BytesIO(file_content),  # File content as stream
                length=len(file_content),  # Size of the file
                content_type=file.content_type,  # File MIME type
            )
            print(f"'{file.filename}' uploaded '{self.bucket_name}' as '{complete_file_id}'.")
            return True

        except S3Error as err:
            # logger.error("Error while uploading file: %s", err)
            print(f"Error uploading file: {err}")
        return False

    def download_file(self, project_id: str, file_id: str):
        """
            TODO
        """
        project_path = self.get_file_path(project_id=project_id)
        file_path = os.path.join(project_path, file_id)
        object_name = f"{project_id}/{file_id}"

        # Ensure the bucket exists
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                print(f"Bucket '{self.bucket_name}' doesn't exist.")
        except S3Error as err:
            print(f"Error checking bucket: {err}")

        # Download the file from MinIO to a certain path
        try:
            self.minio_client.fget_object(self.bucket_name, object_name, file_path)
        except S3Error as err:
            print(f"Error downloading file: {err}")
