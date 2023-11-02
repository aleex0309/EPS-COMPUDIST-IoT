from os import getenv
from json import loads

from kafka import KafkaConsumer


# Turns the output into a dict
def deserializer(value: bytes):
    return loads(value.decode())


if __name__ == "__main__":
    print("Starting CLEANUP SERVICE...")

    consumer = KafkaConsumer(
        "CLEAN",
        bootstrap_servers=[str(getenv("KAFKA_BROKER_HOSTNAME"))],
        value_deserializer=deserializer,
    )

    for msg in consumer:
        print(msg.value)
