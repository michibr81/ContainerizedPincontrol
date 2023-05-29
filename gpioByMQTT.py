import gpioByJson as byJson
import sys
import paho.mqtt.client as mqtt

print(f'First given arg is {sys.argv[0]} second is {sys.argv[1]}')

byJson.initialize("shutterConfiguration.json",runDry=((sys.argv[0] == "dry") or (sys.argv[1] == "dry")))

MQTT_SERVER = 'localhost'
MQTT_PATH = "MBR/automation/shutters"
MQTT_PORT = 1883

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc)) 
    # if connection lost and reconnect subscriptions will be renewed.
    client.subscribe(MQTT_PATH,1)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload)) 

    byJson.controlPinByNameWithLocking(msg.payload)

client = mqtt.Client("mqtt-gpio-byjson-subscriber")
client.on_connect = on_connect
client.on_message = on_message

print("before connect")
client.connect(MQTT_SERVER, MQTT_PORT, 60)

client.loop_forever()