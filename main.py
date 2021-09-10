import paho.mqtt.client as mqtt
import threading
import json
import time
import random
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CaseMQTT/groups/Case/json")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("CaseMQTT","aio_bfGl92GI1YmSMlnM1m9y2MJmpoFa") # Логин и пароль для авторизации
client.connect("io.adafruit.com", 1883, 60) # Адрес и порт брокера, Timeout подключения

thread = threading.Thread(target=client.loop_forever) # Отправляем прослушивание топиков в другой поток
thread.start()                                        # чтобы была возможно

dicts = {'feeds':{"temp":45,"hum":78,"color":"#00AC43"}}

while True:
    time.sleep(3)                                  # Выставляем задержку в 3 секунды
    dicts["feeds"]["temp"] = random.randint(20,30) # Задаём рандомное значение температуры в диапазоне 20-30
    dicts["feeds"]["hum"] = random.randint(50,70)  # Задаём рандомное значение влажности в диапазоне 50-70
    client.publish(topic="CaseMQTT/groups/Case/json",payload=json.dumps(dicts)) # Публикуем Json в топик "CaseMQTT/groups/Case/json"