import importlib
import os, sys, time, json, random
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as pmqttSub
import paho.mqtt.publish as pmqttPub
import numpy as np
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
import repackage
repackage.up()
from utils import simulator, control_center, conect_mqtt
importlib.reload(simulator)
importlib.reload(control_center)
importlib.reload(conect_mqtt)

#numero de ambientes
nEnvironments = 1
timesleep = 10

#inicializando os objetos de simulação dos ambientes e a central de controle
controlC = control_center.ControlCenter(nEnvironments, 1200)
conectMqtt = conect_mqtt.ConectMqtt()
conectMqtt.start_connection_tago()
time.sleep(1)
##################
new_temperatureValues = conectMqtt.subscribe(nEnvironments=nEnvironments, topic_type="temperatura")
print(f"Temperatura inicial: {new_temperatureValues}")
time.sleep(.2)
new_potencyValues = controlC.update_arrayU(new_temperatureValues)
conectMqtt.publish_mosquitto(nEnvironments, topic_type="potencia", data_values=controlC.arrayU)
controlC.update_memory_arrayT_list(new_temperatureValues)

controlC.update_memory_arrayU_list(controlC.arrayU)

time.sleep(.3)
conectMqtt.publish_tago(client=conectMqtt.client, type_data="potencia", data_values=controlC.arrayU, mqttPT=conectMqtt.mqtt_publish_topic)

time.sleep(3)
i = 0
while True:
    i += 1
    if i == 1:
        new_temperatureValues = conectMqtt.subscribe(nEnvironments=nEnvironments, topic_type="temperatura")
        new_potencyValues = controlC.update_arrayU(new_temperatureValues)
        conectMqtt.publish_tago(client=conectMqtt.client, type_data="potencia", data_values=controlC.arrayU, mqttPT=conectMqtt.mqtt_publish_topic)
        controlC.update_memory_arrayT_list(new_temperatureValues)
        
        time.sleep(.3)
        conectMqtt.publish_mosquitto(nEnvironments, topic_type="potencia", data_values=controlC.arrayU)
        time.sleep(.1)
        print(f"memória dos valores de temperatura: {controlC.memory_arrayT[-1]}")
        print(f"memória dos valores de potencia: {controlC.memory_arrayU[-1]}")
        i = 0
        time.sleep(2)
    