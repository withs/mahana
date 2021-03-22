import uuid

from typing import List

from .utils import Utils

class Worker:

    def __init__(self, worker_data, db_con):
        self.name: str
        self.display_name: str
        self.id: str
        self.last_data_sent: str
        self.auth_keys: List
        self.sensors: List
        self.config: dict

        self.db = db_con

        self._from_data(worker_data)

    def _from_data(self, worker_data):
        self.name = worker_data.get("worker_name", None)
        self.display_name = worker_data.get("worker_display_name", None)
        self.id = worker_data.get("worker_id", None)
        self.last_data_sent = worker_data.get("last_data_sent", None)
        self.sensors = None
        self.auth_keys = worker_data.get("auth_keys", None)
        self.config = worker_data.get("worker_config", None)

    @classmethod
    async def create_new_worker(cls, new_worker_data, db_con):

        required_key = ["worker_name"]
        missing_key = []

        for key in required_key:
            if key not in new_worker_data:
                missing_key.append(key)
        if len(missing_key) != 0:
            return (False, missing_key)

        check_if_exist = await db_con.find_worker(
            worker_name=new_worker_data.get("worker_name"),
            check=True
        )
        if check_if_exist is True:
            return (False, "Already exist")

        new_worker = {
            "worker_name": new_worker_data.get("worker_name"),
            "worker_display_name": new_worker_data.get("worker_display_name", "undefined"),
            "worker_id": str(uuid.uuid4()),
            "last_data_sent": None,
            "auth_keys": [Utils.ur_safe_key(key_len=36)],
            "sensors": [],
            "worker_config": {
              "send_data_interval": 0 # prendre cette valuer depuis la config modulaire (config.toml)
            }
        }
        create_new_req = await db_con.add_new_worker(new_worker)
        if create_new_req.result:
            new_worker_obj = cls(new_worker, db_con)
            return (True, new_worker_obj)

        return (False, "db error")

    def __repr__(self):
        return f"<Worker (name={self.name}, id={self.id}, display_name={self.display_name})>"

    async def get_sensors(self):
        if self.sensors is None:
            await self.db.get_worker_sensors(self)
        return self.sensors
