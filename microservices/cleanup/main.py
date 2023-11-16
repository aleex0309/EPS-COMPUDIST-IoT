from operator import truediv
from os import getenv
from json import loads
from time import sleep

from kafka import KafkaConsumer


# Turns the output into a dict
def deserializer(value: bytes) -> dict:
    return loads(value.decode("utf-8"))


if __name__ == "__main__":
    print("Starting CLEANUP SERVICE...")

    hostname = getenv("KAFKA_BROKER_HOSTNAME")
    while True:
        try:
            print(f"Trying to connect to broker {hostname}...", flush=True)
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

    if consumer.bootstrap_connected():
        print("Connection Established!", flush=True)

    for msg in consumer:
        print(f"Recived Value {msg.value}", flush=True)
