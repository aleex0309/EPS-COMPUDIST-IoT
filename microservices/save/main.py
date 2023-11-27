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
url = "http://127.0.0.1:8086"
token = "exampletoken"

print("URL = "+url)
tag = "user1"

client = InfluxDBClient(url=url, token=token, org=org,)
write_api = client.write_api(write_options=SYNCHRONOUS)

kafka_hostname = hostname = os.getenv("KAFKA_BROKER_HOSTNAME")

def deserializer(value: bytes) -> dict:
    return loads(value.decode("utf-8"))

def kafka_clean_connect():
    while True:
        try:
            print(f"Trying to connect to broker {hostname}...", flush=True)
            clean_consumer = KafkaConsumer(
                "", #Topic for clean data
                bootstrap_servers=[str(hostname)],
                value_deserializer=deserializer,
            )

            if clean_consumer.bootstrap_connected():
                break

        except Exception as e:
            print(e, flush=True)

        time.sleep(1)

    if clean_consumer.bootstrap_connected():
        print("Clean Connection Established!", flush=True)

    for msg in clean_consumer:
        print(f"Clean Recived Value {msg.value}", flush=True)

def kafka_raw_connect():
    while True:
        try:
            print(f"Trying to connect to broker {hostname}...", flush=True)
            raw_consumer = KafkaConsumer(
                "", #Topic for raw data
                bootstrap_servers=[str(hostname)],
                value_deserializer=deserializer,
            )

            if raw_consumer.bootstrap_connected():
                break

        except Exception as e:
            print(e, flush=True)

        time.sleep(1)

    if raw_consumer.bootstrap_connected():
        print("Clean Connection Established!", flush=True)

    for msg in raw_consumer:
        print(f"Clean Recived Value {msg.value}", flush=True)

def save_values(value, topic):
    while True:
        time.sleep(10)
        value = random.uniform(20, 25)
        p = Point("measurement").tag("user", tag).field("temperature", value)
        write_api.write(bucket=bucket, record=p)
        print("%s %s" % ("temperature", value))
        time.sleep(1)

if __name__ == "__main__":
    kafka_clean_connect()
    kafka_raw_connect()