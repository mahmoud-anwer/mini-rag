from helpers.config import get_settings

class BaseDataModel:
    def __init__(self, db_client: object):
        """
        Initializes the BaseDataModel instance with a database client and application settings.
        
        Args:
            db_client (object): The database client or connection object used to interact with the database.
        """
        
        # Assign the provided db_client to an instance attribute for database interaction.
        self.db_client = db_client
        
        # Fetch and assign the application settings using the get_settings function.
        # These settings could include configurations like file paths, API keys, etc.
        self.app_settings = get_settings()
