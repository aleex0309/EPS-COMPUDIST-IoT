import os
import time
import token
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
from json import loads

bucket = "mybucket"
org = "myorg"
url = "http://influxdb:8086"
token = "exampletoken"

print("URL = " + url)


cli = InfluxDBClient(
    url=url,
    token=token,
    org=org,
)
write_api = cli.write_api(write_options=SYNCHRONOUS)

kafka_hostname = hostname = os.getenv("KAFKA_BROKER_HOSTNAME")


def deserializer(value: bytes) -> dict:
    return loads(value.decode("utf-8"))


def kafka_connect():
    while True:
        try:
            print(f"Trying to connect to broker {hostname}...", flush=True)
            consumer = KafkaConsumer(
                "save",
                "clean",  # Topic for clean data
                bootstrap_servers=[str(hostname)],
                value_deserializer=deserializer,
                group_id="save",
            )

            if consumer.bootstrap_connected():
                break

        except Exception as e:
            print(e, flush=True)

        time.sleep(1)

    if consumer.bootstrap_connected():
        print("Clean Connection Established!", flush=True)

    for msg in consumer:
        print(f"Received :{msg.value}")
        save_values(msg.value)


def save_values(value):
    p = (
        Point("raw" if value.get("raw") else "clean")
        .tag("gateway", value.get("gateway"))
        .tag("device", value.get("device_name"))
        .field("value", value.get("value"))
    )
    write_api.write(bucket=bucket, record=p)


if __name__ == "__main__":
    kafka_connect()
