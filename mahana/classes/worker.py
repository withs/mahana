import uuid

from typing import List

from .utils import Utils

class Worker:

    aliases = {
        "worker_id": "id",
        "worker_name": "name",
        "worker_display_name": "display_name",
        "worker_config": "config"
    }

    def __init__(self, worker_data, db_con):
        self._name: str= None
        self.display_name: str= None
        self._id: str= None
        self.last_data_sent: str= None
        self.auth_keys: List= None
        self.sensors: List= None
        self.sensors_id: List= None
        self.config: dict= None

        self.db = db_con

        self._from_data(worker_data)

    def _from_data(self, worker_data):
        self._name = worker_data.get("worker_name", None)
        self.display_name = worker_data.get("worker_display_name", None)
        self._id = worker_data.get("worker_id", None)
        self.last_data_sent = worker_data.get("last_data_sent", None)
        self.auth_keys = worker_data.get("auth_keys", None)
        self.sensors_id = worker_data.get("sensors", None)
        self.config = worker_data.get("worker_config", None)

    def to_dict(self):
        worker_dict = {
            "worker_name": self.name,
            "worker_display_name": self.display_name,
            "worker_id": self._id,
            "last_data_sent": self.last_data_sent,
            "sensors": self.sensors_id,
            "auth_keys": self.auth_keys,
            "worker_config": self.config
        }

        return worker_dict

    @classmethod
    async def create_new_worker(cls, new_worker_data, db_con):

        required_key = ["worker_name"]
        missing_key = []

        for key in required_key:
            if key not in new_worker_data:
                missing_key.append(key)
        if len(missing_key) != 0:
            return (False, missing_key)

        if len(new_worker_data.get("worker_name")) == 0:
            return (False, "Blank worker_name")

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
            "sensors_id": new_worker_data.get("sensors"),
            "worker_config": {
              "send_data_interval": 0 # prendre cette valuer depuis la config modulaire (config.toml)
            }
        }

        new_worker_obj = cls(new_worker, db_con)
        create_new_req = await db_con.add_new_worker(new_worker_obj)
        if create_new_req.result:
            return (True, new_worker_obj)

        return (False, "db error")

    async def update_db(self):
        update_req = await self.db.edit_worker(self)

        if update_req.result is True:
            return (True, None)
        return (False, None)

    def __repr__(self):
        return f"<Worker (name={self.name}, id={self.id}, display_name={self.display_name})>"

    def __setitem__(self, key, value):
        if key in self.__dict__ or key in Worker.aliases:
            setattr(self, key, value)

    def __getattribute__(self, name):
        name = Worker.aliases.get(name, name)
        return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        name = Worker.aliases.get(name, name)
        object.__setattr__(self, name, value)

    def __getitem__(self, key):
        return getattr(self, key)


    async def get_sensors(self):
        if self.sensors is None:
            await self.db.get_worker_sensors(self)
        return self.sensors

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, to_set):
        if self._id is None:
            self._id = to_set

    @property
    def name(self):
        return self._name

    async def change_name(self, new_name):
        name_check = await self.db.find_worker(worker_name=new_name, check=True)
        if name_check:
            return self._name
        if len(new_name) != 0:
            self._name = new_name

    async def delete(self):
        delete_req = await self.db.delete_worker(worker=self)
        if delete_req:
            return (True, "worker deleted")
        return (False, "an error while trying to delete worker")
