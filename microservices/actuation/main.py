from json import loads
from os import getenv
from time import sleep
import paho.mqtt.client as client
from kafka import KafkaConsumer

DEVICE_TYPE = {"LIGHT", "PRESENCE_SENSOR", "TEMPERATURE_SENSOR", "HEAT_PUMP"}


kafka_hostname = str(getenv("KAFKA_BROKER_HOSTNAME"))

mqtt_clients = {}


def deserializer(value: bytes) -> dict:
    return loads(value.decode("utf-8"))


def flushed_print(string):
    print(string, flush=True)


def on_connect(client, userdata, flags, rc):
    flushed_print("Connected Succesfully")


def on_disconnect(client, userdata, rc):
    flushed_print("Disconnected")


def on_publish(client, userdata, mid):
    flushed_print(f"SENDED")


if __name__ == "__main__":
    flushed_print("Starting actuation")
    mqtt_client = client.Client()

    # Connect consumer
    while True:
        try:
            print(
                f"(Consumer) Trying to connect to broker {kafka_hostname}...",
                flush=True,
            )
            consumer = KafkaConsumer(
                "actuate",
                bootstrap_servers=[str(kafka_hostname)],
                value_deserializer=deserializer,
            )

            if consumer.bootstrap_connected():
                break

        except Exception as e:
            print(e, flush=True)

        sleep(1)

    mqtt_client.on_connect = on_connect
    mqtt_client.on_disconnect = on_disconnect
    mqtt_client.on_publish = on_publish

    mqtt_client.subscribe("TEMPERATURE_SENSOR")

    mqtt_client.loop_forever()

    for msg in consumer:
        print(f"Recived value from <actuate>: {msg.value}", flush=True)
        hostname: str = msg.value.get("mqtt_hostname")
        clien: client.Client | None = mqtt_clients.get("mqtt_hostname")

        # Check if client is new
        if not clien:
            clien = client.Client()
            clien.on_connect = on_connect
            clien.on_disconnect = on_disconnect
            clien.on_publish = on_publish
            clien.loop_start()
            mqtt_clients.update({hostname: mqtt_client})

        # Check if device is new
        topic = msg.value.get("device_name")

        # Actuate
        value = topic = msg.value.get("device_name")

        # PresenceSensor-> LightBulb: +50 -> 1 / -50 ->0
        # TemperatureSensor -> HeatPump: 18-20 -> 20/ 24-28 -> 24
        match topic:
            case "PRESENCE_SENSOR":
                if value > 50:
                    res = 1
                else:
                    res = 0

                clien.publish("LIGHT", res)

            case "TEMPERATURE_SENSOR":
                if 18 < value and value > 20:
                    res = 20
                elif 24 < value and value > 28:
                    res = 24
                else:
                    continue

                clien.publish("HEAT_PUMP", res)
