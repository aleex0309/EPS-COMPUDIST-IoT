from enum import Enum
from os import error, getenv
import paho.mqtt.subscribe as subscribe
from kafka import KafkaProducer, KafkaConsumer

DEVICE_TYPE={LIGHT, PRESENCE_SENSOR, TEMPERATURE_SENSOR, HEAT_PUMP}

def test_print(client, userdata, message):
    print("%s %s" % (message.topic, message.payload))
    my_producer.send(message.topic, value=message.payload) #Send the information to the kafka broker

if __name__ == "__main__":
    print("Starting gateway")

    my_producer = KafkaProducer(bootstrap_servers=['host.docker.internal:9092'], 
    value_serializer=lambda x: dumps(x).encode('utf-8')) #Connect to the kafka broker
    _deserializer=lambda x: loads(x.decode('utf-8'))

    subscribe.callback(test_print, "+", hostname="host.docker.internal") #Subscribe to the mqtt broker
