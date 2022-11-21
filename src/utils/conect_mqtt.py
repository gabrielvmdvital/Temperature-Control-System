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


def publish(client):

    for x in range(len(temperatura)):
        client.publish("temperatura"+str(x), temperatura[x], 0)
        time.sleep(0.3)


def subscribe():
    for x in range(len(temperatura)):
        client.subscribe("temperatura"+str(x))
#
