# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 13:28:32 2022

@author: LOTFI
"""

# Protocole MQTT : Publier/Supprimer un message retenu sur un topic

import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code => "+mqtt.connack_string(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print("Received message '" + str(msg.payload) + "' on topic '" + msg.topic + 
          "' with QoS " + str(msg.qos))
    
    if msg.retain == 1:
        # Actions à réaliser si le message est un message retenu
        print("This is a retained message from " + str(msg.payload))
        
def on_publish(client, userdata, mid):
    print("-- on_publish callback -- mid: " + str(mid) )

client = mqtt.Client()

client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish

try:
    # Login et password si l’on est avec un broker avec authentification (cf. TP2)
    #client.username_pw_set(username="GX", password="isimaGX")
    
    client.connect("test.mosquitto.org", 1883)

except:
    print("Connection Failed")
    
client.subscribe("isima/#", qos=0)

client.loop_start()

while True:
    # Afin de publier un message retenu, il suffit de rajouter un paramètre lors de la publication
    (rc, mid) = client.publish(topic="isima/GX", payload="If you are new to the topic then _ Welcome _ and if you've been here before then _ Welcome Back !", retain=True)
    
    # Afin de supprimer un message retenu, il suffit de publier un message (payload) vide:
    #(rc, mid) = client.publish(topic="isima/GX", payload="", retain=True)
    
    print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))
    time.sleep(5)