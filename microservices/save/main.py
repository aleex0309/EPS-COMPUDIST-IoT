import random
import os
import ssl
import time
from http import client
import token
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from kafka import KafkaConsumer
from json import loads

bucket = "mybucket"
org = "myorg"
url = "http://influxdb:8086"
token = "exampletoken"

print("URL = "+url)
tag = "user1"

client = InfluxDBClient(url=url, token=token, org=org,)
write_api = client.write_api(write_options=SYNCHRONOUS)

kafka_hostname = hostname = os.getenv("KAFKA_BROKER_HOSTNAME")

def deserializer(value: bytes) -> dict:
    return loads(value.decode("utf-8"))

def kafka_connect():
    while True:
        try:
            print(f"Trying to connect to broker {hostname}...", flush=True)
            consumer = KafkaConsumer(
                "save", #Topic for clean data
                bootstrap_servers=[str(hostname)],
                value_deserializer=deserializer,
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


def save_values(value, topic):
    while True:
        time.sleep(10)
        value = random.uniform(20, 25)
        p = Point("measurement").tag("user", tag).field("temperature", value)
        write_api.write(bucket=bucket, record=p)
        print("%s %s" % ("temperature", value))
        time.sleep(1)

if __name__ == "__main__":
    kafka_connect()
