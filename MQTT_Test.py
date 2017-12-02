#!/usr/bin/env python

import RPi.GPIO as GPIO 
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
# Defining the GPIO ports
LED=22
TRIG=17
ECHO=27
RELAY=18
# MQTT broker info
ServerIP="127.0.0.1"
Port=1883

# Configuration of GPIO ports
GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED, GPIO.OUT) 
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN) 
GPIO.setup(RELAY,GPIO.OUT)

# Starting ultrasonic sensor
GPIO.output(TRIG,False)
time.sleep(2)
# Init states
ledOn = False
relayOn = False
distance = 0


# What the client MQTT will do when connects to the broker
def on_connect(client, userdata,flags,rc):
    print ("Connected with rc: " + str(rc))
    client.subscribe("dev/recv")
# When recv a message from the suscribed topic
def on_message(client, userdata, msg):
    print ("Topic: "+ msg.topic+"\nMessage: "+str(msg.payload))
    if msg.payload == "distance":
    	sensor()
	time.sleep(0.5)
	publish_mqtt(distance)
    elif msg.payload == "toggleLed":
	toggleLed()
	if not ledOn:
		publish_mqttLed("On")
	else:
		publish_mqttLed("Off")
    elif msg.payload == "toggleRelay":
	toggleRelay()
	if relayOn:
                publish_mqttRelay("On")
        else:
                publish_mqttRelay("Off")


# Function to publish from ultrasonic sensor
def publish_mqtt(sensor_data):
	mqttc = mqtt.Client("RaspberryPi")
	mqttc.connect(ServerIP,Port)
	mqttc.publish("dev/distance",distance)
# Function to publish the Led state
def publish_mqttLed(stateL):
	mqttc = mqtt.Client("RaspberryPi")
	mqttc.connect(ServerIP,Port)
	mqttc.publish("dev/LEDState",stateL)
# Function to publish the Relay state
def publish_mqttRelay(stateR):
        mqttc = mqtt.Client("RaspberryPi")
        mqttc.connect(ServerIP,Port)
        mqttc.publish("dev/RelayState",stateR)

def on_publish(mosq,obj,mid):
	print("I have publish somehting!")


# Obtain the distance
def sensor():
	global distance
	GPIO.output(TRIG,True)
	time.sleep(0.00001)
	GPIO.output(TRIG,False)
	while GPIO.input(ECHO)==0:
		pulse_start = time.time()
	while GPIO.input(ECHO)==1:
		pulse_end = time.time()
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance,2)
	print "Distance: ",distance,"cm"
#	GPIO.cleanup()
# Toggle the led
def toggleLed():
	global ledOn
	if ledOn :
		GPIO.output(LED, True)
		ledOn = False
	else:
		GPIO.output(LED, False)
		ledOn = True
# Toggle relay		
def toggleRelay():
        global relayOn
        if relayOn :
                GPIO.output(RELAY, True)
                relayOn = False
        else:
                GPIO.output(RELAY, False)
                relayOn = True

# begin
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(ServerIP, Port, 60)
client.loop_forever()

