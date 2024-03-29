import gpioByJson as gpio
import sys
import paho.mqtt.client as mqtt

MQTT_PATH = ""

def on_connect(client, userdata, flags, rc):
    '''
    The callback when the client receives a CONNACK response from the server.
    if connection lost and reconnect subscriptions will be renewed.
    '''
    print("Connected with result code "+str(rc) + " subscribe to path " + MQTT_PATH) 
    client.subscribe(MQTT_PATH,1)
    sys.stdout.flush()

def on_message(client, userdata, msg):  
    '''
    The callback when a PUBLISH message is received from the server.
    '''
    print(msg.topic+" "+str(msg.payload)) 
    sys.stdout.flush()
    ctrl.controlPinByNameWithLocking(msg.payload.decode('ascii'))

if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='Gpio control by mqtt subscriber')
    parser.add_argument('-S','--SERVER', metavar='path', required=False, default="0.0.0.0",help='the mqtt server to publish')
    parser.add_argument('-P','--PORT', metavar='path', required=False,default=1883, help='the port to publish to')
    parser.add_argument('-p','--path', metavar='path', required=True, help='the mqttt path to publish')
    parser.add_argument('-d','--dryrun', metavar='path', required=False, default=True, help='set to False to run in production mode')
    parser.add_argument('-j','--jsonconfig', metavar='path', required=True, default=True, help='the path to the pin configuration file')
    args = parser.parse_args()

    print(f"Server {args.SERVER}")
    print(f"Port {args.PORT}")
    print(f"Mqtt Path {args.path}")
    print(f"Dry run {args.dryrun}")
    print(f"Pin configuration file {args.jsonconfig}")
    sys.stdout.flush()

    MQTT_PATH = args.path

    ctrl = gpio.gpioByJson(dryRun=(args.dryrun == 'True'))
    ctrl.initialize(args.jsonconfig)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1,"mqtt-gpio-byjson-subscriber")
    client.on_connect = on_connect
    client.on_message = on_message

    print("before connect")
    sys.stdout.flush()
    client.connect(args.SERVER, args.PORT)

    client.loop_forever()
