import gpioByJson as gpio
import sys
import paho.mqtt.client as mqtt

MQTT_SERVER = '0.0.0.0'
MQTT_PATH = "MBR/automation/shutters"
MQTT_PORT = 1883

dryRun=False
configFilePath = "shutterConfiguration.json"
ctrl = gpio.gpioByJson(dryRun=dryRun)
ctrl.initialize(configFilePath)

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) 
    # if connection lost and reconnect subscriptions will be renewed.
    client.subscribe(MQTT_PATH,1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):  
    print(msg.topic+" "+str(msg.payload)) 
    ctrl.controlPinByNameWithLocking(msg.payload.decode('ascii'))

client = mqtt.Client("mqtt-gpio-byjson-subscriber")
client.on_connect = on_connect
client.on_message = on_message

print("before connect")
client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.loop_forever()

