# MQTT_RaspberryPi_GPIO
This was made for UPV-CAR Project. 2017-2018. Carlos N.

IOT with MQTT and Raspberry example. Python 2.7.

Components list:
 * RaspberryPi B+. 
 * HC-SR04 as ultrasonic sensor
 * Red Led
 * Transistor BC548C
 * Some resistors
 * Relay
 
 The RaspberryPi is the broker and a client at the same time.
 I have used a smartwatch as a client to interact with the broker.
 In this example the security is not implemented.
 
 RaspberryPi running 'mosquitto' as a broker. GPIO and Paho libraries used for the client node.
