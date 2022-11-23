import paho.mqtt.client as paho
from utils import conect_mqtt
import sys
import time
import numpy as np
import random

def run():
    env1, env2, env3 = [0], [0], [0]
    client = paho.Client()
    client.on_message = conect_mqtt.onMessage


    if client.connect("localhost", 1883, 60) != 0:
        print("Could not connect to MQTT Broker!")
        sys.exit(-1)
    count = 0
    while True:
        print(f"iteração: 1")
        lst = []
        if count == 10:
            lst = np.array(lst)
            conect_mqtt.publish(client=client, type_data="Temperatura", data_values=lst)
            count = 0
        env1.append(random.randint(15, 28))
        env2.append(random.randint(15, 28))
        env3.append(random.randint(15, 28))
        lst = [env1, env2, env3]
        count += 1
        time.sleep(1)
        
        


if __name__ == "__main__":
    run()