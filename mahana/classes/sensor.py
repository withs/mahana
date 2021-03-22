from typing import List

class Sensor:

    def __init__(self, sensor_data, worker_parent):
        self.id: str
        self.name: str
        self.display_name: str
        self.recorded_data: str
        self.type: str

        self.parent = worker_parent

        self._from_data(sensor_data)

    def _from_data(self, data):
        self.worker_name = data

    def __repr__(self):
        return f"<Sensor (name={self.name}, id={self.id}, type={self.type})>"
