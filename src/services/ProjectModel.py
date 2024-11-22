from .BaseDataModel import BaseDataModel
from models.db_schemes.project import Project
from models.enums.DatabaseEnum import DataBaseEnum


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
