from abc import ABC, abstractmethod
from typing import List
from models import RetrievedDocument

class VectorDBInterface(ABC):
    """
    Abstract base class for interacting with vector databases.

    This class defines the core methods required for managing vector
    database collections and performing vector-based operations.
    """

    @abstractmethod
    def connect(self):
        """
        Establishes a connection to the vector database.
        """

    @abstractmethod
    def disconnect(self):
        """
        Disconnects from the vector database.
        """

    @abstractmethod
    def is_collection_existed(self, collection_name: str) -> bool:
        """
        Checks if a collection exists in the vector database.

        Args:
            collection_name (str): The name of the collection to check.

        Returns:
            bool: True if the collection exists, False otherwise.
        """

    @abstractmethod
    def list_all_collections(self) -> List:
        """
        Lists all the collections in the vector database.

        Returns:
            List: A list of collection names.
        """

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        """
        Retrieves metadata about a specific collection in the vector database.

        Args:
            collection_name (str): The name of the collection to get information for.

        Returns:
            dict: A dictionary containing collection metadata.
        """

    @abstractmethod
    def delete_collection(self, collection_name: str):
        """
        Deletes a collection from the vector database.

        Args:
            collection_name (str): The name of the collection to delete.
        """

    @abstractmethod
    def create_collection(self, collection_name: str,
                          embedding_size: int,
                          do_reset: bool = False):
        """
        Creates a new collection in the vector database.

        Args:
            collection_name (str): The name of the collection to create.
            embedding_size (int): The size of the vectors to be stored in the collection.
            do_reset (bool, optional): Whether to reset the collection if it already exists. Defaults to False.
        """

    @abstractmethod
    def insert_one(self, collection_name: str,
                   text: str, vector: list,
                   metadata: dict = None,
                   record_id: str = None):
        """
        Inserts a single record into a collection.

        Args:
            collection_name (str): The name of the collection to insert the record into.
            text (str): The text to insert.
            vector (list): The vector representation of the text.
            metadata (dict, optional): Additional metadata associated with the record. Defaults to None.
            record_id (str, optional): An optional unique record identifier. Defaults to None.
        """

    @abstractmethod
    def insert_many(self, collection_name: str,
                    texts: list,
                    vectors: list,
                    metadata: list = None,
                    record_ids: list = None,
                    batch_size: int = 50):
        """
        Inserts multiple records into a collection.

        Args:
            collection_name (str): The name of the collection to insert the records into.
            texts (list): A list of texts to insert.
            vectors (list): A list of vector representations of the texts.
            metadata (list, optional): A list of metadata for the records. Defaults to None.
            record_ids (list, optional): A list of unique record identifiers. Defaults to None.
            batch_size (int, optional): The number of records to insert per batch. Defaults to 50.
        """

    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: list, limit: int) -> List[RetrievedDocument]:
        """
        Searches for similar vectors within a collection using a query vector.

        Args:
            collection_name (str): The name of the collection to search.
            vector (list): The vector to use as the query.
            limit (int): The maximum number of results to return.

        Returns:
            List: A list of search results.
        """
