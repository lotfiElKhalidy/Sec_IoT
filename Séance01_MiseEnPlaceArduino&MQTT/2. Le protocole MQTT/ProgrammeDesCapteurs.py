# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 14:02:40 2022

@author: LOTFI
"""

# MQTT : Programme des "capteurs"

import paho.mqtt.client as mqtt
import random as ra
import time

# Define variable
MQTT_HOST_NAME = "…" # Host of broker MQTT
MQTT_HOST_PORT = "…." # Port of broker MQTT

MQTT_USERNAME = "…." # Username of user log (here PROF log)
MQTT_PASSWORD = "…." # Password of user log (here PROF log)

MQTT_CLIENT_ID = "prof_ISIMA" # Client ID
MQTT_LAST_WILL_TOPIC = "isima/LWT" # Topic of Last Will Message
MQTT_LAST_WILL_MSG = "Lost Connection" # Message of Last Will Message
MQTT_QOS = 0 # Quality of service
MQTT_CLEAR_SESSION = True # Flag Clean Session
MQTT_RETAINED_MSG = True # Flag Retained Session

MQTT_CLEAR_RETAINED = True

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("-- on_connect callback -- Connection returned result: " + mqtt.connack_string(rc))
    
    if rc == 0:
        global Connected # Use global variable
        Connected = True # Signal connection

# The callback for when the client publish on server.
def on_publish(client, userdata, mid):
    print("-- on_publish callback -- mid: " + str(mid) )

# The callback for when the client receives a message from server.
def on_message(client, userdata, msg):
    print("-- on_message callback -- Received message '" + str(msg.payload) + "' on topic '" + msg.topic +
          "' with QoS " + str(msg.qos))
    if msg.retain == 1:
        print("This is a retained message")

Connected = False #global variable for the state of the connection

client = mqtt.Client(MQTT_CLIENT_ID,MQTT_CLEAR_SESSION)
client.will_set(MQTT_LAST_WILL_TOPIC,MQTT_LAST_WILL_MSG, 0, False)

client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message

try:
    #client.username_pw_set(MQTT_USERNAME,MQTT_PASSWORD)
    client.connect(MQTT_HOST_NAME,MQTT_HOST_PORT)

except:
    print("Connection failed")

client.loop_start()

while Connected != True: # Wait for connection
     time.sleep(0.1)

client.subscribe("$SYS/broker/version") # Sample of system topic

if MQTT_CLEAR_RETAINED:
    (rc, mid) = client.publish(topic="isima/G1", payload="", qos=MQTT_QOS, retain=True)
    (rc, mid) = client.publish(topic="isima/G2", payload="", qos=MQTT_QOS, retain=True)
    (rc, mid) = client.publish(topic="isima/G3", payload="", qos=MQTT_QOS, retain=True)
    (rc, mid) = client.publish(topic="isima/G4", payload="", qos=MQTT_QOS, retain=True)

while True:
    tempG1 = 15 + ra.uniform(-10, 10)
    (rc, mid) = client.publish(topic="isima/G1", payload=tempG1, qos=MQTT_QOS, 
                               retain=MQTT_RETAINED_MSG)
    print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))
 
tempG2 = 15 + ra.uniform(-10, 10)
(rc, mid) = client.publish(topic="isima/G2", payload=tempG2, qos=MQTT_QOS, 
                           retain=MQTT_RETAINED_MSG)
print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))
 
tempG3 = 15 + ra.uniform(-10, 10)
(rc, mid) = client.publish(topic="isima/G3", payload=tempG3, qos=MQTT_QOS, 
                           retain=MQTT_RETAINED_MSG)
print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))
 
tempG4 = 15 + ra.uniform(-10, 10)
(rc, mid) = client.publish(topic="isima/G4", payload=tempG4, qos=MQTT_QOS, 
                           retain=MQTT_RETAINED_MSG)
print("Error return from publish of mid = " + str(mid) +" : " + mqtt.error_string(rc))
 
time.sleep(3)