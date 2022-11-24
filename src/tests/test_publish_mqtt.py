import numpy as np
import os, sys, time, json, tago, random
import paho.mqtt.client as mqtt
SCRIPT_DIR = os.path.dirname(os.path.abspath("src/utils/conect_mqtt.py"))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from utils import conect_mqtt





def publish(client, type_data: str, data_values: np.ndarray, mqttPT: str) -> None:
    lst_dict = []
    for index in range(len(data_values)):
        lst_dict.append({"variable": f"{type_data}_environment_{index+1}", 
                        "unit": "F", "value": data_values[index]})

    for index in range(len(lst_dict)):
        client.publish(mqttPT, json.dumps(lst_dict[index]))
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

    timeCount = 1
    iteration = 1
    lst = []
    publish(client=client, type_data="Temperatura", data_values=env1+env2+env3, mqttPT=mqtt_publish_topic)
    while True:
        print(f"Interation: {iteration}") 
        if timeCount == 10:
            env1.append(random.randint(18, 22))
            env2.append(random.randint(18, 22))
            env3.append(random.randint(18, 22))
            lst =[env1[-1], env2[-1], env3[-1]]
            conect_mqtt.publish2(client=client, type_data="Temperatura", data_values=lst, mqttPT=mqtt_publish_topic)
            lst = []
            timeCount = 0

       # print(lst)
        
        iteration += 1
        timeCount += 1
        time.sleep(1)

        

    print("Data sent to TagoIO platform")

if __name__ == "__main__":
    run()