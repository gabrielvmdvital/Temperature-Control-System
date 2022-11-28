from utils import simulator, control_center, conect_mqtt
import repackage
import importlib
import os
import sys
import time
import json
import random
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
repackage.up()
importlib.reload(simulator)
importlib.reload(control_center)

# numero de ambientes
nEnvironments = 1
timesleep = 10
# inicializando os objetos de simulação dos ambientes e a central de controle
sim = simulator.Simulator(nEnvironments)


conectMqtt = conect_mqtt.ConectMqtt(sim)
conectMqtt.start_connection_tago()

client = mqtt.Client()
client.connect("localhost")



print(f"Temperatura inicial: {sim.arrayT}")

conectMqtt.subscribe(client=client, topic="potencia")
conectMqtt.message_callback(
    topic="potencia", func=conectMqtt.call_back_temperatura)


conectMqtt.publish_mosquitto(
    client = client, topic = "temperatura", payload = sim.arrayT)
