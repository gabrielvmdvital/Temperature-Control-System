import numpy as np
import paho.mqtt.client as paho
import sys
import time
import json

client = paho.Client()


def onMessage(client, userdate, msg):
    print(msg.topic + ": " + msg.payload.decode())


client = paho.Client()
client.on_message = onMessage


if client.connect("localhost", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)


def publish(client, type_data: str, data_values: np.ndarray, mqttPT: str) -> None:
    lst_dict = []
    for index in range(len(data_values)):
        lst_dict.append({"variable": f"{type_data}_environment_{index+1}", 
                        "unit": "F", "value": data_values[index]})

    for index in range(len(lst_dict)):
        client.publish(mqttPT, json.dumps(lst_dict[index]))
        time.sleep(.3)

def publish2(client, type_data: str, data_values: np.ndarray, mqttPT: str) -> None:
    lst_dict = []
    data_unit = {"temperatura": "°C",
                     "potencia": "BTU"}
    for index in range(len(data_values)):
        #lst_dict.append({"variable": f"{type_data}_environment_{index+1}", 
        #                "unit": "F", "value": data_values[index]})
        
        element = {"variable": f"{type_data.capitalize()}_environment_{index+1}", 
                        "unit": data_unit[type_data.lower()].capitalize(), "value": data_values[index]}
        lst_dict.append(element)
        client.publish(mqttPT, json.dumps(element))
        time.sleep(.3)
        print(lst_dict)

def subscribe(client, type_data: str, data_values: np.ndarray):
    """
    """
    for nEnviroments_values in range(len(data_values)):
        client.subscribe(f"{type_data} {nEnviroments_values+1}")
        time.sleep(0.3)

