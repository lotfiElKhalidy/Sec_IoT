# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 13:56:41 2022

@author: LOTFI
"""

# Protocole MQTT : S'abonner à un topic

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code => " + mqtt.connack_string(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

# Une fois abonné à un topic, on peut recevoir des LWT ou 
#  des Retained messages de la part des clients abonnés au topic
def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic +
          "' with QoS " + str(msg.qos))

MQTT_CLIENT_ID = "lotfi"
MQTT_CLEAR_SESSION = True # ou False

client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=MQTT_CLEAR_SESSION)
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_connect = on_connect

try:
    # Login et password si l’on est avec un broker avec authentification (cf. TP2)
    #client.username_pw_set(username="GX", password="isimaGX")
    
    client.connect("test.mosquitto.org", 1883)
    
except:
    print("Connection Failed")

# On est abonné au topic 'isima/GX'
client.subscribe("isima/GX", qos=0)

client.loop_forever()