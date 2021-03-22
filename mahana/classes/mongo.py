from dataclasses import make_dataclass
import asyncio

from configs.config import DatabaseConfig
from rich import print

from .worker import Worker
from .sensor import Sensor


class Mongo:
    def __init__(self, mongo_client):
        self.mongo_db_client = mongo_client
        self.db = self.mongo_db_client[DatabaseConfig.BASE_DB]
        self.data_class_resp = make_dataclass('DbResult', ["result", "result_data"])


    async def find_auth_by_key(self, key: str):
        # {"auth_keys": {$in: ["abc"]}}

        collections_list = await self.db.list_collection_names()
        for collection in collections_list:
            collection = self.db.get_collection(collection)
            collection_querry = await collection.find_one({"auth_keys": {"$in": [key]}},{"_id": False})

            if collection_querry is not None:
                return self.data_class_resp(True, collection_querry)
        return self.data_class_resp(False, collection_querry)

    async def add_new_worker(self, worker_dict: dict) -> None:

        worker_collection = self.db[f"""worker-{worker_dict["worker_id"]}"""]

        add_new_worker_req = await worker_collection.insert_one(worker_dict)

        if add_new_worker_req.acknowledged:
            return self.data_class_resp(True, add_new_worker_req.inserted_id)
        return self.data_class_resp(False, None)

    async def find_worker(self, worker_name: str= None, worker_id: str= None, check: bool= False):
        """Find a worker by his name or id"""

        collection_querry = None
        collection = None

        if worker_id is None:
            collections_list = await self.db.list_collection_names()
            for collection in collections_list:
                collection = self.db.get_collection(collection)
                collection_querry = await collection.find_one({"worker_name": str(worker_name)})
                if collection_querry is not None:
                    worker_id = collection_querry["worker_id"]
            if worker_id is None:
                return None

        worker_coll = collection or self.db[f"worker-{worker_id}"]
        worker_data = collection_querry or await worker_coll.find_one({"worker_id": worker_id})

        if not check:
            worker_obj = Worker(worker_data, self)
            return worker_obj
        return True


    async def get_worker_sensors(self, worker):

        sensors = []

        worker_coll = self.db[f"worker-{worker.id}"]
        sensors_list_id = await worker_coll.find_one({"worker_id": worker.id})

        for sensor_id in sensors_list_id["sensors"]:
            sensor_data = await worker_coll.find_one({"censor_id": sensor_id})
            sensor_obj = Sensor(sensor_data, worker)
            sensors.append(sensor_obj)

        worker.sensors = sensors
        return sensors
