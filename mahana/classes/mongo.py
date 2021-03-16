from configs.config import DatabaseConfig


class Mongo:
    def __init__(self, mongo_client):
        self.mongo_db_client = mongo_client
        self.db = self.mongo_db_client[DatabaseConfig.BASE_DB]


    async def add_new_worker(self, name: str, display_name: str, worker_id: str) -> None:

        worker_collection = self.db[f"worker-{worker_id}"]

        document = {
            "woker_name": name,
            "worker_display_name": display_name,
            "worker_id": worker_id,
            "last_data_sent": None,
            "auth_keys": [],
            "sensors": [],

        }
        await worker_collection.insert_one(document)

    async def find_auth_by_key(self, key: str) -> bool:
        # {"auth_keys": {$in: ["abc"]}}

        collections_list = await self.db.list_collection_names()
        for collection in collections_list:
            collection = self.db.get_collection(collection)
            collection_querry = await collection.find_one({"auth_keys": {"$in": [key]}})
            if collection_querry is not None:
                return True
            return False

    async def find_by_worker_name(self, worker_name: str) -> bool:

        collections_list = await self.db.list_collection_names()
        for collection in collections_list:
            collection = self.db.get_collection(collection)
            collection_querry = await collection.find_one({"worker_name": str(worker_name)})
            if collection_querry is not None:
                return True
            return False
