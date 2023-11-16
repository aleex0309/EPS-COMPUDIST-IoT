from operator import truediv
from os import getenv
from json import loads
from time import sleep

from kafka import KafkaConsumer


# Turns the output into a dict
def deserializer(value: bytes):
    return loads(value.decode())


if __name__ == "__main__":
    print("Starting CLEANUP SERVICE...")

    hostname = getenv("KAFKA_BROKER_HOSTNAME")
    while True:
        try:
            print(f"Trying to connect to broker {hostname}...", flush=True)
            consumer = KafkaConsumer(
                "CLEAN",
                bootstrap_servers=[str(getenv("KAFKA_BROKER_HOSTNAME"))],
                value_deserializer=deserializer,
            )

            if consumer.bootstrap_connected():
                break

        except Exception:
            pass

        sleep(1)
    if consumer.bootstrap_connected():
        print("Connection Established!")

    for msg in consumer:
        print(msg.value)
