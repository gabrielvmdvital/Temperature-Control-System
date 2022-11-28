import importlib
import os, sys, time, json, random
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as pmqttSub
import paho.mqtt.publish as pmqttPub
import numpy as np
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import simulator, control_center, conect_mqtt
importlib.reload(simulator)
importlib.reload(control_center)
importlib.reload(conect_mqtt)

cnt = conect_mqtt.ConectMqtt()
ev1 = np.array([10, 20, 30])
while True:

    time.sleep(.5)
    
    cnt.publish_mosquitto(nEnvironments=3, topic_type="temperatura", data_values=ev1)
