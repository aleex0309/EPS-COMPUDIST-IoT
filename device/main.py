from enum import Enum
from os import error, getenv


class DeviceTypes(Enum):
    LIGHT = "LIGHT"
    PRESENCE_SENSOR = "PRESENCE_SENSOR"
    TEMPERATURE_SENSOR = "TEMPERATURE_SENSOR"
    HEAT_PUMP = "HEAT_PUMP"


if __name__ == "__main__":
    device_type = getenv("DEVICE_TYPE")

    if device_type not in [e.value for e in DeviceTypes]:
        print("Device type not registered")
        exit(-1)
