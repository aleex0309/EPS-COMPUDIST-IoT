from os import getenv
from device import devices


if __name__ == "__main__":
    device_type = getenv("DEVICE_TYPE")

    if device_type not in devices:
        print(f"Device type {device_type} not registered")
        exit(-1)

    device = devices[device_type]
    device.connect(getenv("BROKER_HOSTNAME"), device.name)
    device.start()
