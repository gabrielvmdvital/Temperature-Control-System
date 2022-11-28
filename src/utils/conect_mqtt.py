import numpy as np
import paho.mqtt.client as mqtt
import paho.mqtt.subscribe as pmqttSub
import paho.mqtt.publish as pmqttPub
import sys
import time
import json
import tago
import random
import repackage
repackage.up()


class ConectMqtt:

    def __init__(self, service, host: str = "localhost", broker_tago_port: int = 1883, mqtt_keep_alive_tago: int = 60,
                 device_tago_token: str = 'cc8d3e6a-eab9-4b3f-8cf7-3a0cb850f50d', broker_tago="mqtt.tago.io",
                 mqtt_publish_topic: str = "tago/data/post", mqtt_username: str = 'eduardoalexandree.ps@gmail.com',
                 mqtt_password: str = 'cc8d3e6a-eab9-4b3f-8cf7-3a0cb850f50d', ) -> None:

        self.controlC = service
        self.__host = host
        self.__port = broker_tago_port
        self.__mqtt_keep_alive_tago = mqtt_keep_alive_tago
        self.__device_tago_token = device_tago_token
        self.__broker_tago_port = broker_tago_port
        self.__broker_tago = broker_tago
        self.mqtt_publish_topic = mqtt_publish_topic
        self.__mqtt_username = mqtt_username
        self.__mqtt_password = mqtt_password
        self.client = None

    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("[STATUS] Connected to MQTT broker. Result: " + str(rc))
        else:
            print("Client is not conected ")

    def onMessage(self, client, userdate, msg):
        print(f"{msg.topic} : {msg.payload.decode()}")

    def start_connection_tago(self):
        conected = False
        menssagerecieved = False
        print("[STATUS] Initializing MQTT...")
        self.client = mqtt.Client()
        self.client.username_pw_set(self.__mqtt_username, self.__mqtt_password)
        self.client.on_connect = self.on_connect
        self.client.connect(self.__broker_tago, self.__broker_tago_port)

    def publish_tago(self, client, type_data: str, data_values: np.ndarray, mqttPT: str) -> None:
        print("[STATUS] - Publishing to Tago.io")
        data_unit = {"temperatura": "°C",
                     "potencia": "BTU"}
        for index in range(len(data_values)):
            element = {"variable": f"{type_data.capitalize()}_environment_{index+1}",
                       "unit": data_unit[type_data.lower()].capitalize(), "value": int(data_values[index])}
            time.sleep(.1)
            self.client.publish(mqttPT, json.dumps(element))

    def publish_mosquitto(self, client, topic: str, payload):
        print("[STATUS] - Publishing to Mosquitto")
        bit_payload = payload.tobytes()
        client.publish(f"{topic.capitalize()}", bit_payload)

    def subscribe(self, client, topic: str):
        print("[STATUS] - Subscrite from Mosquitto")
        client.subscribe(f"{topic.capitalize()}")

    def message_callback(self, client, topic: str, func):
        client.message_callback_add(topic.capitalize(), func)

    def call_back_potencia(self, client, userdata, message):

        new_temperatureValues = np.frombuffer(
            message.payload, dtype=np.float32)
        print(f"Temperatura inicial: {new_temperatureValues}")

        new_potencyValues = self.service.update_arrayU(new_temperatureValues)
        new_potencyBit = new_potencyValues.tobytes()
        client.publish("potencia", payload=new_potencyBit)
        time.sleep(2)
        # conectMqtt.publish_tago(client=conectMqtt.client, type_data="potencia",
        # data_values=controlC.arrayU, mqttPT=conectMqtt.mqtt_publish_topic)

    def call_back_temperatura(self, client, userdata, message):

        new_potenciaValues = np.frombuffer(
            message.payload, dtype=np.float32)
        print(f"Potencia inicial: {new_potenciaValues}")

        new_tempValues = self.service.update_arrayT(new_potenciaValues)
        new_tempBit = new_tempValues.tobytes()
        client.publish("temp", payload=new_tempBit)
        time.sleep(2)
        # conectMqtt.publish_tago(client=conectMqtt.client, type_data="potencia",
        # data_values=controlC.arrayU, mqttPT=conectMqtt.mqtt_publish_topic)


if __name__ == "__main__":

    clt = ConectMqtt()
    clt.start_connection_tago()
    env1, env2, env3 = [random.randint(15, 28)], [random.randint(15, 28)], [
        random.randint(15, 28)]
    timeCount = 1
    iteration = 1
    lst = []
    while True:
        print(f"Interation: {iteration}")
        if timeCount == 10:
            env1.append(random.randint(18, 22))
            env2.append(random.randint(18, 22))
            env3.append(random.randint(18, 22))
            lst = [env1[-1], env2[-1], env3[-1]]
            clt.publish_tago(client=clt.client, type_data="Temperatura",
                             data_values=lst, mqttPT=clt.mqtt_publish_topic)

            print(lst)
            lst = []
            timeCount = 0

       # print(lst)

        iteration += 1
        timeCount += 1
        time.sleep(1)
