# Import what is necessary to create a thread

import time
import pycom
from pysense import Pysense
import machine
from network import WLAN
from mqtt import MQTTClient
from SI7006A20 import SI7006A20

pycom.heartbeat(False)
# pycom.rgbled(0xFF0000) # white
py = Pysense()

si = SI7006A20(py)

def sub_cb(topic, msg):
   print(msg)

wlan = WLAN(mode=WLAN.STA)
wlan.connect("KNAA", auth=(WLAN.WPA2, "KNAA2374"), timeout=5000)


while not wlan.isconnected():
    machine.idle()
print("Connected to Wifin")

client = MQTTClient("blablou", "mqtt.eclipse.org",user="", password="", port=1883)
client.set_callback(sub_cb)
client.connect()
client.subscribe(topic="testadp")
while True:
    temp = si.temperature()
    print("Temperature: " + str(si.temperature())+ " deg C")
    if (temp > 31):
        pycom.rgbled(0x200000)
        client.publish(topic="testadp", msg="T'es pas ok")
    else:
        pycom.rgbled(0x002000)
        client.publish(topic="testadp", msg="T'es ok")
    time.sleep(3)







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
