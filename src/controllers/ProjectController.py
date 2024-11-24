import os
from controllers.BaseController import BaseController


class ProjectController(BaseController):
    """
    Controller class for handling project-related operations.

    Inherits from BaseController to utilize common functionalities.
    """

    def __init__(self):
        """
        Initializes the ProjectController instance.

        Calls the constructor of the BaseController to set up the application settings.
        """
        super().__init__()

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
