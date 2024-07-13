import os
import random
import string
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

    def generate_random_string(self, length: int = 12) -> str:
        """
        Generates a random string of specified length.

        This method creates a random string consisting of lowercase letters and digits.

        Args:
            length (int): The length of the random string to be generated. Defaults to 12.

        Returns:
            str: A random string of the specified length.
        """
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
