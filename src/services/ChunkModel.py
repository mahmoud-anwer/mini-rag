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

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Class method to create an instance of the class and initialize the collection.

        This method is used to:
            1. Create an instance of the class with the provided database client.
            2. Initialize the collection associated with the instance by calling the `init_collection` method.

        Args:
            db_client (object): The database client to interact with the database.

        Returns:
            object: The newly created instance of the class with the initialized collection.
        """
        # Create an instance of the class using the provided db_client
        instance = cls(db_client)

        # Initialize the collection for the instance
        await instance.init_collection()

        # Return the created instance
        return instance

    async def init_collection(self):
        """
        Initializes the chunk collection in the database by ensuring it exists.
        If the collection does not exist, it will be created, and the appropriate indexes
        will be added based on the DataChunk model's index definitions.

        This method performs the following actions:
            1. Checks if the chunk collection exists in the database.
            2. If the collection does not exist, it is created.
            3. Retrieves the index definitions from the DataChunk model.
            4. Creates each index in the chunk collection, ensuring proper indexing
               for the fields and enforcing uniqueness where specified.
        """
        # Retrieve a list of all collection names in the database
        all_collections = await self.db_client.list_collection_names()

        # Check if the specific collection (PROJECT_COLLECTION_NAME) does not exist
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            # If the collection does not exist, create it by referencing the collection name
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]

            # Retrieve the indexes for the DataChunk model
            indexes = DataChunk.get_indexes()

            # Iterate over the list of indexes and create each index on the collection
            # pylint: disable=R0801
            for index in indexes:
                await self.collection.create_index(
                    index["key"],        # The fields for the index (e.g., field_name: 1 for ascending)
                    name=index["name"],  # The name of the index (e.g., "index_name")
                    unique=index["unique"]  # Whether the index should enforce uniqueness
                )

    async def create_chunk(self, chunk: DataChunk):
        """
        Creates a new chunk in the database.

        Inserts a single chunk into the collection and updates its ID with the database-generated ID.

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

    async def get_poject_chunks(self, project_id: ObjectId, page_no: int=1, page_size: int=50):
        """
        Retrieves chunks associated with a specific project ID.

        Retrieves a paginated list of chunks for the given project ID. The results are
        returned based on the page number and page size provided.

        Args:
            project_id (ObjectId): The ID of the project whose chunks are to be retrieved.
            page_no (int): The page number for pagination. Defaults to 1.
            page_size (int): The number of chunks per page. Defaults to 50.

        Returns:
            list: A list of DataChunk objects for the specified project.
        """
        records = await self.collection.find({
                    "chunk_project_id": project_id
                }).skip(
                    (page_no-1) * page_size
                ).limit(page_size).to_list(length=None)

        return [
            DataChunk(**record)
            for record in records
        ]
