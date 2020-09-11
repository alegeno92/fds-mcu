import json


class SensorValue:

    def __init__(self, module, sensor, value, timestamp):
        self.module = module
        self.sensor = sensor
        self.value = value
        self.timestamp = timestamp

    def format(self):
        return json.dumps({
            "module": self.module,
            "sensor": self.sensor,
            "value": self.value,
            "timestamp": self.timestamp
        })

    def pretty_format(self):
        return json.dumps({
            "module": self.module,
            "sensor": self.sensor,
            "value": self.value,
            "timestamp": self.timestamp},
            sort_keys=True,
            indent=4
        )

    def stocazzo_format(self):
        value_type = str(type(self.value)).split("'")[1]

        if value_type == 'str':
            value_type = 'string'

        return {
            "module": self.module,
            "sensor": self.sensor,
            "value_type": value_type,
            "value": self.value,
            "timestamp": self.timestamp
        }


class Reader:

    def read(self) -> SensorValue:
        pass
