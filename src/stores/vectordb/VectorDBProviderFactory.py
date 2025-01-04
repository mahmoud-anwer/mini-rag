from controllers.BaseController import BaseController
from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBEnums


class VectorDBProviderFactory:
    """
    Factory class for creating instances of vector database providers.

    This class is responsible for creating and initializing the appropriate
    vector database provider based on the configuration and specified provider type.
    """

    def __init__(self, config):
        """
        Initializes the VectorDBProviderFactory with a configuration object.

        Args:
            config (object): The configuration object containing database settings.
        """
        self.config = config
        self.base_controller = BaseController()

    def create(self, provider: str):
        """
        Creates and returns an instance of a vector database provider based on the provided provider type.

        Args:
            provider (str): The type of vector database provider to create (e.g., "QDRANT").

        Returns:
            object: An instance of the specified vector database provider, or None if the provider type is not recognized.

        Raises:
            ValueError: If the provider type is not recognized.
        """
        # if provider == VectorDBEnums.QDRANT.value:
        #     db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_PATH)

        #     return QdrantDBProvider(
        #         db_path=db_path,
        #         distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
        #     )

        if provider == VectorDBEnums.QDRANT.value:
            db_url = self.config.VECTOR_DB_URL

            return QdrantDBProvider(
                db_url=db_url,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
            )

        return None
