import numpy as np
import paho.mqtt.client as paho
import sys
import time

client = paho.Client()


def onMessage(client, userdate, msg):
    print(msg.topic + ": " + msg.payload.decode())


client = paho.Client()
client.on_message = onMessage


if client.connect("localhost", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)


def publish(client, type_data: str, data_values: np.ndarray):
    """
    """
    for nEnviroments in range(len(data_values)):
        for data in range(len(data_values[nEnviroments])):
            client.publish(f"{type_data} environment {nEnviroments+1}", data_values[data], 0)
            time.sleep(0.3)


def subscribe(client, type_data: str, data_values: np.ndarray):
    """
    """
    for nEnviroments_values in range(len(data_values)):
        client.subscribe(f"{type_data} {nEnviroments_values+1}")
        time.sleep(0.3)

