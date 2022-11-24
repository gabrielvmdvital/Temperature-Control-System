import paho.mqtt.client as mqtt
import sys
import random
import time
import json
import tago
import numpy as np
# Definitions
# put here your device token

def publish(client, type_data: str, data_values: np.ndarray, mqttPT: str) -> None:
    lst_dict = []
    for index in range(len(data_values)):
        lst_dict.append({"variable": f"{type_data}_{index+1}", 
                        "unit": "F", "value": data_values[index]})
    for data in lst_dict:
        client.publish(mqttPT, json.dumps(data))
        time.sleep(.3)
    print(lst_dict)     


def run():
    device_token = 'cc8d3e6a-eab9-4b3f-8cf7-3a0cb850f50d'

    broker = "mqtt.tago.io"
    broker_port = 1883
    mqtt_keep_alive = 60

    # MQTT publish topic must be tago/data/post
    mqtt_publish_topic = "tago/data/post"

    # put any name here, TagoIO doesn't validate this username.
    mqtt_username = 'eduardoalexandree.ps@gmail.com'

    # MQTT password must be the device token (TagoIO does validate this password)
    mqtt_password = device_token

    # Callback - MQTT broker connection is on

    env1, env2, env3 = [random.randint(15, 28)], [random.randint(15, 28)], [random.randint(15, 28)]

    def on_connect(client, userdata, flags, rc):
        print("[STATUS] Connected to MQTT broker. Result: " + str(rc))


    # Main program
    print("[STATUS] Initializing MQTT...")
    client = mqtt.Client()
    client.username_pw_set(mqtt_username, mqtt_password)
    client.on_connect = on_connect
    client.connect(broker, broker_port, mqtt_keep_alive)

    timeCount = 0
    iteration = 1
    lst = []
    initedT = env1+env2+env3
    publish(client=client, type_data="Temperatura", data_values=initedT, mqttPT=mqtt_publish_topic)
    while True:
        timeCount += 1
        print(f"Interation: {iteration}") 
        if timeCount == 2:
            env1.append(random.randint(15, 28))
            env2.append(random.randint(15, 28))
            env3.append(random.randint(15, 28))
            lst =[env1[-1], env2[-1], env3[-1]]
            publish(client=client, type_data="Temperatura", data_values=lst, mqttPT=mqtt_publish_topic)
            lst = []
            timeCount = 0

       # print(lst)
        
        iteration += 1
        time.sleep(1)

        

    print("Data sent to TagoIO platform")

if __name__ == "__main__":
    run()