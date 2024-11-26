from models import DataBaseEnum, Project
from .BaseDataModel import BaseDataModel


class ProjectModel(BaseDataModel):
    """
    Model class for managing project records in the database.

    Inherits from BaseDataModel to leverage common database functionalities.
    """

    def __init__(self, db_client: object):
        """
        Initializes the ProjectModel instance.

        Args:
            db_client (object): The database client instance used to interact with the database.
        """
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

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
        Initializes the project collection in the database by ensuring it exists.
        If the collection does not exist, it will be created, and the appropriate indexes
        will be added based on the Project model's index definitions.

        This method performs the following actions:
            1. Checks if the project collection exists in the database.
            2. If the collection does not exist, it is created.
            3. Retrieves the index definitions from the Project model.
            4. Creates each index in the project collection, ensuring proper indexing
            for the fields and enforcing uniqueness where specified.
        """
        # Retrieve a list of all collection names in the database
        all_collections = await self.db_client.list_collection_names()

        # Check if the specific collection (PROJECT_COLLECTION_NAME) does not exist
        if DataBaseEnum.COLLECTION_PROJECT_NAME.value not in all_collections:
            # If the collection does not exist, create it by referencing the collection name
            self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]

            # Retrieve the indexes for the Project model
            indexes = Project.get_indices()

            # Iterate over the list of indexes and create each index on the collection
            # pylint: disable=R0801
            for index in indexes:
                await self.collection.create_index(
                    index["key"],        # The fields for the index (e.g., field_name: 1 for ascending)
                    name=index["name"],  # The name of the index (e.g., "index_name")
                    unique=index["unique"]  # Whether the index should enforce uniqueness
                )

    async def create_project(self, project: Project):
        """
        Creates a new project in the database.

        Inserts the project into the collection and updates its ID with the database-generated ID.

        Args:
            project (Project): The project to be added to the database.

        Returns:
            Project: The project with its updated ID.
        """
        result = await self.collection.insert_one(project.dict(by_alias=True, exclude_unset=True))
        project.id = result.inserted_id
        return project

    async def get_project_or_create_one(self, project_id: str):
        """
        Retrieves an existing project by its ID or creates a new one if it doesn't exist.

        Searches the collection for a project with the given ID. If no matching project is found, 
        a new project is created and returned.

        Args:
            project_id (str): The unique identifier for the project.

        Returns:
            Project: The retrieved or newly created project.
        """
        record = await self.collection.find_one({
            "project_id": project_id
        })

        if record is None:
            # Create a new project if it doesn't exist
            project = Project(project_id=project_id)
            project = await self.create_project(project=project)
            return project

        return Project(**record)

    async def get_all_projects(self, page: int = 1, page_size: int = 10):
        """
        Retrieves all projects from the database with pagination.

        Fetches projects in the specified page, limiting the projects number based on the page size.

        Args:
            page (int): The page number to fetch. Defaults to 1.
            page_size (int): The number of projects to fetch per page. Defaults to 10.

        Returns:
            tuple: A list of projects and the total number of pages.
        """
        # Count the total number of documents in the collection
        total_documents = await self.collection.count_documents({})

        # Calculate the total number of pages
        total_pages = total_documents // page_size
        if total_documents % page_size > 0:
            total_pages += 1

        # Fetch the projects for the specified page
        cursor = self.collection.find().skip((page - 1) * page_size).limit(page_size)
        projects = []
        async for document in cursor:
            projects.append(
                Project(**document)
            )
        return projects, total_pages
