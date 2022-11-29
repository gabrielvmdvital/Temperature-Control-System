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
from utils import simulator, control_center, conect_mqtt
importlib.reload(simulator)
importlib.reload(control_center)
importlib.reload(conect_mqtt)


global topic
topic = "Potencia"
global ctrl_center
global ctrl
# numero de ambientes

nEnvironments = 4
timesleep = 10
potency_limit=1200
conectMqtt = mqtt.Client()
conectMqtt.connect("localhost")
ctrl = conect_mqtt.ConectMqtt()
ctrl.start_connection_tago()
ctrl_center = control_center.ControlCenter(
    nEnvironment=nEnvironments, potency_limit=potency_limit, Ttarget=30.0)

def call_back_potencia(client, userdata, message):

    new_temperatureValues = np.frombuffer(
        message.payload, dtype=np.float32)
    print(f"New Temperature array: {new_temperatureValues}")

    new_potencyValues = ctrl_center.update_arrayU(new_temperatureValues)
    new_potencyBit = new_potencyValues.tobytes()
    ctrl.publish_tago(ctrl.client_tago, "Potencia", new_potencyValues*potency_limit, ctrl.mqtt_publish_topic)
    client.publish("Potencia", payload=new_potencyBit)
    
    time.sleep(.5)

ctrl.publish_tago(ctrl.client_tago, "Potencia", ctrl_center.arrayU*potency_limit, ctrl.mqtt_publish_topic)
conectMqtt.subscribe("Temperatura")
conectMqtt.message_callback_add("Temperatura", call_back_potencia)


conectMqtt.loop_forever()
