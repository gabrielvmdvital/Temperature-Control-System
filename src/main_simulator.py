import importlib
import os, sys, time, json, random
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as subscribe
import paho.mqtt.publish as publish
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import simulator, control_center, conect_mqtt
importlib.reload(simulator)
importlib.reload(control_center)

#numero de ambientes
nEnvironments = 3
timesleep = 10

#inicializando os objetos de simulação dos ambientes e a central de controle
sim = simulator.Simulator(nEnvironments)
conectMqtt = conect_mqtt.ConectMqtt()
conectMqtt.start_connection_tago()
print(sim.arrayT)
i = 0
conectMqtt.publish_tago(client=conectMqtt.client, type_data="Temperatura", data_values=sim.arrayT, mqttPT=conectMqtt.mqtt_publish_topic)
time.sleep(.3)
conectMqtt.publish_mosquitto(nEnvironments, topic_type="Temperatura", data_values=sim.arrayT)
time.sleep(2)
while True:
    i += 1
    if i == timesleep+1:        
        print(f"memória dos valores de temperatura: {sim.memory_list}")
        new_potencyValue = conectMqtt.subscribe(nEnvironments=nEnvironments, topic_type="potencia")
        time.sleep(.3)
        sim.update_arrayT(new_potencyValue)
        sim.update_memory_list(sim.arrayT)
        conectMqtt.publish_tago(client=conectMqtt.client, type_data="Temperatura", data_values=sim.arrayT, mqttPT=conectMqtt.mqtt_publish_topic)
        time.sleep(.3)
        conectMqtt.publish_mosquitto(nEnvironments, topic_type="Temperatura", data_values=sim.arrayT)
        time.sleep(.5)
        print(f"Novo valor de temperatura: {sim.arrayT}")
        time.sleep(1)
        i = 0
    