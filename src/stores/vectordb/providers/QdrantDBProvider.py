from typing import List
from qdrant_client import models, QdrantClient
from utils.logger import logger
from models import RetrievedDocument
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums


class QdrantDBProvider(VectorDBInterface):
    """
    QdrantDBProvider is a concrete implementation of the VectorDBInterface using Qdrant as the vector database.

    This class handles interaction with the Qdrant vector database, including connecting, disconnecting,
    checking collections, and inserting or searching records.
    """

    def __init__(self, db_url: str, distance_method: str):
        """
        Initializes the QdrantDBProvider with the given database path and distance method.

        Args:
            db_path (str): The path to the Qdrant database.
            distance_method (str): The distance metric to use (e.g., 'cosine' or 'dot').
        """
        self.client = None
        self.db_url = db_url
        self.distance_method = None

        if distance_method == DistanceMethodEnums.COSINE.value:
            self.distance_method = models.Distance.COSINE
        elif distance_method == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT

    def connect(self):
        """
        Establishes a connection to the Qdrant database.
        """
        self.client = QdrantClient(url=self.db_url)

    def disconnect(self):
        """
        Disconnects from the Qdrant database by setting the client to None.
        """
        self.client = None

    def is_collection_existed(self, collection_name: str) -> bool:
        """
        Checks if a collection exists in the database.

        Args:
            collection_name (str): The name of the collection to check.

        Returns:
            bool: True if the collection exists, False otherwise.
        """
        return self.client.collection_exists(collection_name=collection_name)

    def list_all_collections(self) -> List:
        """
        Retrieves a list of all collections in the database.

        Returns:
            List: A list of collection names.
        """
        return self.client.get_collections()

    def get_collection_info(self, collection_name: str) -> dict:
        """
        Retrieves information about a specific collection.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            dict: The collection information.
        """
        return self.client.get_collection(collection_name=collection_name)

    def delete_collection(self, collection_name: str):
        """
        Deletes a collection from the database if it exists.

        Args:
            collection_name (str): The name of the collection to delete.
        """
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        return None

    def create_collection(self, collection_name: str, embedding_size: int, do_reset: bool = False):
        """
        Creates a new collection in the database.

        Args:
            collection_name (str): The name of the collection to create.
            embedding_size (int): The size of the vector embeddings.
            do_reset (bool, optional): Whether to reset an existing collection. Defaults to False.

        Returns:
            bool: True if the collection was created, False if the collection already exists.
        """
        if do_reset:
            _ = self.delete_collection(collection_name=collection_name)

        if not self.is_collection_existed(collection_name):
            _ = self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=embedding_size,
                    distance=self.distance_method
                )
            )
            return True

        return False

    # pylint: disable=too-many-arguments
    def insert_one(self, collection_name: str, text: str, vector: list, metadata: dict = None, record_id: str = None):
        """
        Inserts a single record into the specified collection.

        Args:
            collection_name (str): The name of the collection to insert into.
            text (str): The text content to store.
            vector (list): The vector representation of the text.
            metadata (dict, optional): Additional metadata to store with the record.
            record_id (str, optional): A custom ID for the record.

        Returns:
            bool: True if the record was successfully inserted, False otherwise.
        """
        if not self.is_collection_existed(collection_name):
            logger.error("Cannot insert new record into non-existing collection: %s", {collection_name})
            return False

        try:
            _ = self.client.upload_records(
                collection_name=collection_name,
                records=[
                    models.Record(
                        id=[record_id],
                        vector=vector,
                        payload={
                            "text": text, "metadata": metadata
                        }
                    )
                ]
            )
        except Exception as e:
            logger.error("Error while inserting record: %s", e)
            return False

        return True

    # pylint: disable=too-many-arguments
    def insert_many(self, collection_name: str, texts: list, vectors: list, metadata: list = None,
                    record_ids: list = None, batch_size: int = 50):
        """
        Inserts multiple records into the specified collection in batches.

        Args:
            collection_name (str): The name of the collection to insert into.
            texts (list): A list of texts to store.
            vectors (list): A list of vectors corresponding to the texts.
            metadata (list, optional): A list of metadata corresponding to the texts.
            record_ids (list, optional): A list of custom record IDs.
            batch_size (int, optional): The size of each batch. Defaults to 50.

        Returns:
            bool: True if all records were successfully inserted, False otherwise.
        """
        if metadata is None:
            metadata = [None] * len(texts)

        if record_ids is None:
            record_ids = list(range(0, len(texts)))

        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size

            batch_texts = texts[i:batch_end]
            batch_vectors = vectors[i:batch_end]
            batch_metadata = metadata[i:batch_end]
            batch_record_ids = record_ids[i:batch_end]

            batch_records = [
                models.Record(
                    id=batch_record_ids[x],
                    vector=batch_vectors[x],
                    payload={
                        "text": batch_texts[x], "metadata": batch_metadata[x]
                    }
                )
                for x in range(len(batch_texts))
            ]

            try:
                _ = self.client.upload_records(
                    collection_name=collection_name,
                    records=batch_records,
                )
            except Exception as e:
                logger.error("Error while inserting record: %s", e)
                return False

        return True

    def search_by_vector(self, collection_name: str, vector: list, limit: int = 5):
        """
        Searches for records in the specified collection that are similar to the provided vector.

        Args:
            collection_name (str): The name of the collection to search.
            vector (list): The vector to search for similar records.
            limit (int, optional): The number of similar records to return. Defaults to 5.

        Returns:
            List: A list of search results, or an empty list if no results were found.
        """
        results = self.client.search(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit
        )

        if not results or len(results) == 0:
            return None

        return [
            RetrievedDocument(**{
                "score": result.score,
                "text": result.payload["text"]
            })
            for result in results
        ]
