# Import what is necessary to create a thread

import time
import pycom
from pysense import Pysense
import machine
from network import WLAN
#from wifi import WiFi
from mqtt import MQTTClient
from SI7006A20 import SI7006A20

IBMorgID='4dvbez' # Identifiant de l'instance 'IoT PLatform' sur 6 caractères
deviceType='Pycom' # Nom du 'Device Type' défini dans le IoT Platform
deviceID='4321' # ID du device (4 dernieres caractères du SSID)
deviceToken='fzKYk0T3ZFK_(NDj?X' # Token (mot de passe) défini pour le device dans le Iot Platform

pycom.heartbeat(False)
# pycom.rgbled(0xFF0000) # white
py = Pysense()

si = SI7006A20(py)

#wifi = WiFi()

def sub_cb(topic, msg):
   print(msg)

#Connexion
wlan = WLAN(mode=WLAN.STA)
wlan.connect("KNAA", auth=(WLAN.WPA2, "KNAA2374"), timeout=5000)

print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
print("Dew point: "+ str(si.dew_point()) + " deg C")

# Syntaxe pour envoyer un paquet MQTT à IBM Cloud
client = MQTTClient("d:"+IBMorgID+":"+deviceType+":"+deviceID, IBMorgID +".messaging.internetofthings.ibmcloud.com", user="use-token-auth", password=deviceToken, port=1883)
print(client.connect())


while not wlan.isconnected():
    machine.idle()
print("Connected to Wifin")


while True:
    print("Sending")
    mqttMsg = '{'
    mqttMsg = mqttMsg + '"t":' + str(si.temperature())
    mqttMsg = mqttMsg + '}'
    client.publish(topic="iot-2/evt/data/fmt/json", msg=mqttMsg)
    time.sleep(1)


# client = MQTTClient("blablou", "mqtt.eclipse.org",user="", password="", port=1883)
# client.set_callback(sub_cb)
# client.connect()
# client.subscribe(topic="testadp")
# while True:
#     temp = si.temperature()
#     print("Temperature: " + str(si.temperature())+ " deg C")
#     if (temp > 31):
#         pycom.rgbled(0x200000)
#         client.publish(topic="testadp", msg="T'es pas ok")
#     else:
#         pycom.rgbled(0x002000)
#         client.publish(topic="testadp", msg="T'es ok")
#     time.sleep(3)







# import time
# from machine import Pin
# from onewire import DS18X20
# from onewire import OneWire
#
# # DS18B20 data line connected to pin P10
# ow = OneWire(Pin('P10'))
# temp = DS18X20(ow)
#
# while True:
#     print(temp.read_temp_async())
#     time.sleep(1)
#     temp.start_conversion()
#     time.sleep(1)
