from bson.objectid import ObjectId
from models import DataBaseEnum, Asset
from .BaseDataModel import BaseDataModel


class AssetModel(BaseDataModel):
    """
    Model class for managing asset records in the database.

    Inherits from BaseDataModel to leverage common database functionalities.
    """

    def __init__(self, db_client: object):
        """
        Initializes the AssetModel instance.

        Args:
            db_client (object): The database client instance used to interact with the database.
        """
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]

    @classmethod
    async def create_instance(cls, db_client: object):
        """
        Asynchronously creates an instance of the AssetModel.

        Args:
            db_client (object): The database client instance.

        Returns:
            AssetModel: An initialized instance of AssetModel.
        """
        instance = cls(db_client)
        await instance.init_collection()
        return instance

    async def init_collection(self):
        """
        Ensures the collection for assets exists in the database.

        If the collection does not exist, it is created and the necessary indexes are applied.
        """
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )

    async def create_asset(self, asset: Asset):
        """
        Inserts a new asset document into the collection.

        Args:
            asset (Asset): The asset object to be inserted.

        Returns:
            Asset: The inserted asset object, with the `id` field populated.
        """
        result = await self.collection.insert_one(asset.dict(by_alias=True, exclude_unset=True))
        asset.id = result.inserted_id
        return asset

    async def get_all_project_assets(self, asset_project_id: str, asset_type: str):
        """
        Retrieves all assets for a specific project and asset type.

        Args:
            asset_project_id (str): The ID of the project associated with the assets.
            asset_type (str): The type of assets to retrieve.

        Returns:
            list[Asset]: A list of Asset objects matching the criteria.
        """
        records = await self.collection.find({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id,
            "asset_type": asset_type,
        }).to_list(length=None)

        return [
            Asset(**record)
            for record in records
        ]
