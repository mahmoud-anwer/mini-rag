from enum import Enum

class DataBaseEnum(Enum):
    """
    Enum class for defining database collection names.

    This class is used to store the collection names for different entities in the database.
    Each attribute represents a collection in the database with its corresponding name as a string.
    """

    # Collection name for projects in the database
    COLLECTION_PROJECT_NAME = "projects"

    # Collection name for chunks in the database
    COLLECTION_CHUNK_NAME = "chunks"

    # Collection name for assets in the database
    COLLECTION_ASSET_NAME = "assets"
