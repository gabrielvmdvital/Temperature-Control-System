import importlib
import os, sys, time, json, random
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as pmqttSub
import paho.mqtt.publish as pmqttPub
import numpy as np
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import simulator, control_center
importlib.reload(simulator)
importlib.reload(control_center)


def run(nEnvironment: int, timesleep=10) -> None:

    #intancia dos objetos simulator e controlCenter
    sim = simulator.Simulator(nEnvironment=nEnvironment)
    ctrlCenter = control_center.ControlCenter(nEnvironment=nEnvironment, potency_limit=1200)
    i = 1
    iteration = 1
    current_temperature_values = sim.post_temperature_status()
    while True and iteration < 20:
        
        if  i == timesleep+1:
            print(f"[STATUS] - iteration {iteration}")     
            #envio dos dados de temperaturas atuais nos ambientes pelo simulador para a central de controle
            #armazenamento dos dados de temperaturas atuais nos ambientes
            #calculo e update na memoria das novas potencias para os respectivos ambientes
            
            ctrlCenter.update_arrayU(current_temperature_values)
            ctrlCenter.update_memory_arrayU_list(ctrlCenter.arrayU)
            #envio das novas potencias para os respectivos ambientes
            current_potency_values = ctrlCenter.post_upadate_arrayU()
            #atualização dos novos valores de temperatura dos ambientes
            sim.update_arrayT(current_potency_values)
            current_temperature_values = sim.post_temperature_status()
            ctrlCenter.update_memory_arrayT_list(current_temperature_values)
            i = 0
            iteration += 1
            time.sleep(1)

        i+=1
        

if __name__ == "__main__":
    run(nEnvironment=5, timesleep = 100)