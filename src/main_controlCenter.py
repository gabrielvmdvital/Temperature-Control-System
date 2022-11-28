from utils import simulator, control_center, conect_mqtt
import repackage
import importlib
import os
import sys
import time
import json
import random
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as pmqttSub
import paho.mqtt.publish as pmqttPub
import numpy as np
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
repackage.up()
importlib.reload(simulator)
importlib.reload(control_center)
importlib.reload(conect_mqtt)

# numero de ambientes
nEnvironments = 1
timesleep = 10

ctrl = control_center.ControlCenter(
    nEnvironment=nEnvironments, potency_limit=1200)


conectMqtt = conect_mqtt.ConectMqtt(ctrl)
conectMqtt.start_connection_tago()


# inicializando os objetos de simulação dos ambientes e a central de controle Mosquitto
client = mqtt.Client()
client.connect("localhost")
##################


conectMqtt.subscribe(client=client, topic="temperatura")
conectMqtt.message_callback(
    topic="temperatura", func=conectMqtt.call_back_potencia)


client.loop_forever()
