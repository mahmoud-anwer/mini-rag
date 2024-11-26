import os
from helpers import get_settings


class BaseController:
    """
    Base controller class providing common functionalities for other controllers.

    This class initializes application settings and directory paths,
    and includes utility methods for generating random strings.

    Attributes:
        app_settings: Application settings retrieved from the get_settings function.
        base_dir: The base directory of the application.
        files_dir: The directory path for storing files.
    """

    def __init__(self):
        """
        Initializes the BaseController with application settings and directory paths.
        """
        self.app_settings = get_settings()

        # Getting the root directory "/the/whole/path/mini-rag/src"
        self.base_dir = os.path.dirname(os.path.dirname(__file__))

        # Getting the files directory path "/the/whole/path/mini-rag/src/assets/files"
        self.files_dir = os.path.join(self.base_dir, "assets/files")

    def get_file_path(self, project_id: str) -> str:
        """
        Retrieves or creates the directory path for a given project.

        This method constructs the directory path based on the project ID and
        ensures the directory exists. If it doesn't, the method creates it.

        Args:
            project_id (str): The ID of the project for which to get the file path.

        Returns:
            str: The directory path for the specified project.
        """
        # Construct the project directory path using the base files directory and project ID
        project_dir = os.path.join(self.files_dir, project_id)

        # Check if the project directory exists, and create it if it does not
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)

        # Return the project directory path
        return project_dir
