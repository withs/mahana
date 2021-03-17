from dataclasses import make_dataclass

from configs.config import DatabaseConfig


class Mongo:
    def __init__(self, mongo_client):
        self.mongo_db_client = mongo_client
        self.db = self.mongo_db_client[DatabaseConfig.BASE_DB]
        self.data_class_resp = make_dataclass('DbResult', ["result", "result_data"])


    async def add_new_worker(self, worker_dict: dict) -> None:

        worker_collection = self.db[f"""worker-{worker_dict["worker_id"]}"""]


        a = await worker_collection.insert_one(worker_dict)
        print(a)

    async def find_auth_by_key(self, key: str) -> bool:
        # {"auth_keys": {$in: ["abc"]}}

        collections_list = await self.db.list_collection_names()
        for collection in collections_list:
            collection = self.db.get_collection(collection)
            collection_querry = await collection.find_one({"auth_keys": {"$in": [key]}},{"_id": False})

            if collection_querry is not None:
                return self.data_class_resp(True, collection_querry)
        return self.data_class_resp(False, collection_querry)



    async def find_by_worker_name(self, worker_name: str):


        collections_list = await self.db.list_collection_names()
        for collection in collections_list:
            collection = self.db.get_collection(collection)
            collection_querry = await collection.find_one({"worker_name": str(worker_name)})
            if collection_querry is not None:
                return self.data_class_resp(True, collection_querry)
        return self.data_class_resp(False, collection_querry)
