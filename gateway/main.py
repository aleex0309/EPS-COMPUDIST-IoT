from json import dumps
from os import getenv
from time import sleep
import paho.mqtt.client as client
from kafka import KafkaProducer

DEVICE_TYPE = {"LIGHT", "PRESENCE_SENSOR", "TEMPERATURE_SENSOR", "HEAT_PUMP"}

producer: KafkaProducer


def serializer(value):
    return dumps(value).encode("utf-8")


def flushed_print(string):
    print(string, flush=True)


def on_message(client, userdata, message):
    flushed_print(f"{message.topic} {message.payload}")

    message.payload = str(message.payload)

    producer.send("save", message.payload)
    producer.send("clean", message.payload)


def on_connect(client, userdata, flags, rc):
    flushed_print("Connected Succesfully")


def on_disconnect(client, userdata, rc):
    flushed_print("Disconnected")


if __name__ == "__main__":
    flushed_print("Starting gateway")

    mtqq_hostname = str(getenv("MQTT_HOSTNAME"))
    kafka_hostname = str(getenv("KAFKA_BROKER_HOSTNAME"))
    flushed_print(f"Connected to host: {mtqq_hostname}")

    mqtt_client = client.Client()

    while True:
        try:
            print(f"Trying to connect to broker {kafka_hostname}...", flush=True)
            producer = KafkaProducer(
                bootstrap_servers=[kafka_hostname],
                value_serializer=serializer,
            )

            if producer.bootstrap_connected():
                break

        except Exception:
            pass
        sleep(1)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_message = on_message

    mqtt_client.connect(host=mtqq_hostname)
    mqtt_client.subscribe("TEMPERATURE_SENSOR")

    mqtt_client.loop_forever()
