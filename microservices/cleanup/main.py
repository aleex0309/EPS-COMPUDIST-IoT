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
    group_id = getenv("GROUP_ID")
    partition_id = getenv("PARTITION_ID")

    if group_id:
        print(f"Consumer group: {group_id}")

    # Connect consumer
    while True:
        try:
            print(f"(Consumer) Trying to connect to broker {hostname}...", flush=True)
            consumer = KafkaConsumer(
                "save",
                bootstrap_servers=[str(hostname)],
                value_deserializer=deserializer,
                group_id=group_id,
                auto_offset_reset="latest",
                enable_auto_commit=True,
            )

            if consumer.bootstrap_connected():
                break

        except Exception as e:
            print(e, flush=True)

        sleep(1)

    print("Connection Established(Consumer)!", flush=True)

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

        print("Connection Established(Producer)!", flush=True)

    for msg in consumer:
        print(f"Recived value from <save>: {msg.value}", flush=True)
        if filter_value(msg.value):
            msg.value.update({"raw": False})
            producer.send("clean", msg.value)
            print(f"Sended to <clean>: {msg.value}", flush=True)
