from os import getenv
from json import loads, dumps
from time import sleep

from kafka import KafkaConsumer, KafkaProducer


# Turns the output into a dict
def deserializer(value: bytes) -> dict:
    return loads(value.decode("utf-8"))


def serializer(value):
    return dumps(value).encode("utf-8")


def filter_value(value: dict):
    reading = value["value"]
    if value["device_name"] == "PRESENCE_SENSOR":
        if 0 < reading and reading < 100:
            return True

    if value["device_name"] == "TEMPERATURE_SENSOR":
        if -18 < reading and reading < 28:
            return True

    return False


if __name__ == "__main__":
    print("Starting CLEANUP SERVICE...")

    hostname = getenv("KAFKA_BROKER_HOSTNAME")

    # Connect consumer
    while True:
        try:
            print(f"(Consumer) Trying to connect to broker {hostname}...", flush=True)
            consumer = KafkaConsumer(
                "clean",
                bootstrap_servers=[str(hostname)],
                value_deserializer=deserializer,
            )

            if consumer.bootstrap_connected():
                break

        except Exception as e:
            print(e, flush=True)

        sleep(1)

    # Connect producer
    while True:
        try:
            print(f"(Producer) Trying to connect to broker {hostname}...", flush=True)
            producer = KafkaProducer(
                bootstrap_servers=[hostname],
                value_serializer=serializer,
            )

            if producer.bootstrap_connected():
                break

        except Exception:
            pass
        sleep(1)

    if consumer.bootstrap_connected():
        print("Connection Established(Consumer)!", flush=True)

    if producer.bootstrap_connected():
        print("Connection Established(Producer)!", flush=True)

    for msg in consumer:
        print(f"Recived value from <clean>: {msg.value}", flush=True)
        if filter_value(msg.value):
            producer.send("save", msg.value)
            print(f"Sended to <save>: {msg.value}", flush=True)
