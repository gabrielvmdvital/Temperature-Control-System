import importlib
import os, sys, time, json, random
import paho.mqtt.client as mqtt
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import simulator, control_center
importlib.reload(simulator)
importlib.reload(control_center)

#numero de ambientes
nEnvironments = 3

#inicializando os objetos de simulação dos ambientes e a central de controle
sim = simulator.Simulator(nEnvironments)
controlC = control_center.ControlCenter(nEnvironments, 500)

#enviando os dados de temperatura nos ambientes
controlC.update_memory_arrayT_list(sim.post_temperature_status())
#calculando os novos valores de potencia e temperatura
controlC.update_arrayU()
sim.update_arrayT(controlC.post_upadate_arrayU())
print(f"memória dos valores de potencia : {controlC.memory_arrayU}")
print(sim.memory_list)
