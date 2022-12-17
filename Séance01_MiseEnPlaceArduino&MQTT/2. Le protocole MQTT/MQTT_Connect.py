# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 10:35:56 2022

@author: LOTFI
"""

# Protocole MQTT : Connexion à un broker 

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code => " + mqtt.connack_string(rc))

client = mqtt.Client()
client.on_connect = on_connect

try:
    # Login et password si l’on est avec un broker avec authentification (cf. TP2)
    #client.username_pw_set(username="GX", password="isimaGX")
    
    client.connect("test.mosquitto.org", 1883)
    # 1883 : connexion annonyme (non authentifiée)
    
except:
    print("Connection Failed")

client.loop_forever()
