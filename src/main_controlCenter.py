import importlib
import os, sys, time, json, random
import paho.mqtt.client as mqtt
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import simulator, control_center, conect_mqtt
importlib.reload(simulator)
importlib.reload(control_center)
importlib.reload(conect_mqtt)

#numero de ambientes
nEnvironments = 3

#inicializando os objetos de simulação dos ambientes e a central de controle
controlC = control_center.ControlCenter(nEnvironments, 1200)