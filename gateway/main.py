from enum import Enum
from os import error, getenv
import paho.mqtt.client as client

DEVICE_TYPE={"LIGHT", "PRESENCE_SENSOR", "TEMPERATURE_SENSOR", "HEAT_PUMP"}

def test_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))

def on_connect(client, userdata, flags, rc):
    print("Connected Succesfully")

def on_disconnect(client, userdata, rc):
    print("Disconnected")

if __name__ == "__main__":
    print("Starting gateway")

    host = str(getenv("MQTT_HOSTNAME"))
    print(host)

    mqtt_client = client.Client()
    mqtt_client.connect(host=host)
    mqtt_client.subscribe("TEMPERATURE_SENSOR")
    mqtt_client.on_connect = on_connect # ERROR AQUI
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_message = test_print
    mqtt_client.loop_forever()
