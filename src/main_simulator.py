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
import numpy as np
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import simulator, control_center, conect_mqtt
repackage.up()
importlib.reload(simulator)
importlib.reload(control_center)

# numero de ambientes
nEnvironments = 4
timesleep = 10
global sim
global topic
global ctrl
topic = "Temperatura"
# inicializando os objetos de simulação dos ambientes e a central de controle
sim = simulator.Simulator(nEnvironments)
ctrl = conect_mqtt.ConectMqtt()
ctrl.start_connection_tago()

conectMqtt = mqtt.Client()
conectMqtt.connect("localhost")

def call_back_temperatura(client, userdata, message):

        new_potenciaValues = np.frombuffer(
            message.payload, dtype=np.float32)
        print(f"Potencia inicial: {new_potenciaValues}")

        new_tempValues = sim.update_arrayT(new_potenciaValues)
        new_tempValues = new_tempValues.astype('float32')
        new_tempBit = new_tempValues.tobytes()
        client.publish("Temperatura", payload=new_tempBit)
        ctrl.publish_tago(ctrl.client_tago, "Temperatura", new_tempValues, ctrl.mqtt_publish_topic)
        time.sleep(.5)


print(f"Temperatura inicial: {sim.arrayT.astype(np.float32)}")
byteArray = sim.arrayT.tobytes()
conectMqtt.subscribe("Potencia")
conectMqtt.message_callback_add("Potencia", call_back_temperatura)

#conectMqtt.publish_mosquitto(client = conectMqtt, topic = "temperatura", payload = sim.arrayT)
ctrl.publish_tago(ctrl.client_tago, "Temperatura", sim.arrayT, ctrl.mqtt_publish_topic)
conectMqtt.publish("Temperatura", payload=byteArray)

conectMqtt.loop_forever()