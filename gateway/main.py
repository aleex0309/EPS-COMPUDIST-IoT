from operator import truediv
from os import getenv
import paho.mqtt.client as client

DEVICE_TYPE = {"LIGHT", "PRESENCE_SENSOR", "TEMPERATURE_SENSOR", "HEAT_PUMP"}


def flushed_print(string):
    print(string, flush=True)


def on_message(client, userdata, message):
    flushed_print(f"{message.topic} {message.payload}")


def on_connect(client, userdata, flags, rc):
    flushed_print("Connected Succesfully")


def on_disconnect(client, userdata, rc):
    flushed_print("Disconnected")


if __name__ == "__main__":
    flushed_print("Starting gateway")

    host = str(getenv("MQTT_HOSTNAME"))
    flushed_print(f"Connected to host: {host}")

    mqtt_client = client.Client()

    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_message = on_message

    mqtt_client.connect(host=host)
    mqtt_client.subscribe("TEMPERATURE_SENSOR")

    mqtt_client.loop_forever()
