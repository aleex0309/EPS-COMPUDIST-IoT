from random import randrange
from time import sleep

# MQTT Imports
from paho.mqtt.client import Client


class Device:
    name: str
    isActuator: bool
    valid_range: tuple[int, int]
    reading: int

    client: Client

    def __init__(
        self, name: str, isActuator: bool, valid_range: tuple[int, int]
    ) -> None:
        self.name = name
        self.isActuator = isActuator
        self.valid_range = valid_range
        self.reading = self._generate_value()

        # Initialize client
        self.client = Client()

    # Starts loop
    def start(self):
        if not self.client.is_connected():
            print("Can't start, device not connected to MQTT server")
            exit(-1)

        while True:
            if not self.isActuator:
                self._handle_sensor()

    def connect(self, hostname, topic):
        self.client.connect(hostname)

        if self.isActuator:
            self.client.subscribe(topic)
            self.client.on_message = self._on_message

    # Generates a random value between the specified range
    def _generate_value(self):
        return randrange(*self.valid_range)

    # Handles subscribe callback
    def _on_message(self, client, userdata, message):
        print(f"RECIVED: {message.payload}")
        self.reading = message.payload
        pass

    # Sends the new value and sleeps 1sec
    def _handle_sensor(self):
        self.reading = self._generate_value()
        self._publish_wrapper(self.reading)
        sleep(1)

    def _publish_wrapper(self, message):
        self.client.publish(self.name, f"{message}")


# Predefined devices
devices = {}
devices.update({"LIGHT": Device("LIGHT", True, (0, 1))})
devices.update({"PRESENCE_SENSOR": Device("PRESENCE_SENSOR", False, (-10, 110))})
devices.update({"TEMPERATURE_SENSOR": Device("TEMPERATURE_SENSOR", False, (15, 30))})
devices.update({"HEAT_PUMP": Device("HEAT_PUMP", True, (15, 30))})
