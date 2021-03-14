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
