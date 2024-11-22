from bson.objectid import ObjectId
from pymongo import InsertOne
from models import DataChunk, DataBaseEnum
from .BaseDataModel import BaseDataModel


class ChunkModel(BaseDataModel):
    """
    Model class for managing data chunks in the database.

    Inherits from BaseDataModel to utilize common database functionalities.
    """

    def __init__(self, db_client: object):
        """
        Initializes the ChunkModel instance.

        Args:
            db_client (object): The database client instance to interact with the database.
        """
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

    async def create_chunk(self, chunk: DataChunk):
        """
        Creates a new chunk in the database.

        Inserts a single chunk in the collection and updates its ID with the database-generated ID.

        Args:
            chunk (DataChunk): The chunk to be added to the database.

        Returns:
            DataChunk: The chunk with its updated ID.
        """
        result = await self.collection.insert_one(chunk.dict(by_alias=True, exclude_unset=True))
        chunk.id = result.inserted_id
        return chunk

    async def get_chunck(self, chunk_id: str):
        """
        Retrieves a chunk from the database using its ID.

        Searches for a chunk in the collection by its ObjectId.

        Args:
            chunk_id (str): The ID of the chunk to retrieve.

        Returns:
            DataChunk or None: The retrieved chunk, or None if no match is found.
        """
        result = await self.collection.find_one({
            "_id": ObjectId(chunk_id)
        })

        if result is None:
            return None
        return DataChunk(**result)

    async def insert_many_chunks(self, chunks: list, batch_size: int = 2):
        """
        Inserts multiple chunks into the database in batches.

        Performs bulk insertion of chunks, breaking them into batches of a specified size.

        Args:
            chunks (list): A list of DataChunk objects to insert.
            batch_size (int): The number of chunks to include in each batch. Defaults to 2.

        Returns:
            int: The total number of chunks inserted.
        """
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i+batch_size]
            operations = [
                InsertOne(chunk.dict(by_alias=True, exclude_unset=True))
                for chunk in batch
            ]

            await self.collection.bulk_write(operations)

        return len(chunks)

    async def delete_chunks_by_project_id(self, project_id: ObjectId):
        """
        Deletes all chunks associated with a specific project ID.

        Removes chunks from the collection where the project ID matches the provided ID.

        Args:
            project_id (ObjectId): The ID of the project whose chunks are to be deleted.

        Returns:
            int: The number of chunks deleted.
        """
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
        })
        return result.deleted_count
