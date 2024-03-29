# ContainerizedPincontrol

This project aims to get the RaspBerryPi pin control python 
library [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) running 
in a docker container.

The implementation [gpioByJson.py](gpioByJson.py) abstracts the control 
of raspberry pi pins by an configuration.json 
file (see [shutterConfiguration.json](shutterConfiguration.json)) 
which maps commands to pin-control advices.

The logic in [gpioByMQTT.py](gpioByMQTT.py) is responsible for 
connecting to mqtt and calling methods from [gpioByJson.py](gpioByJson.py)
by inserting the mqtt-message payload.

## Configuration

### Dockerfile

The used image is based on `python`. 
The [Dockerfile](Dockerfile) provides the settings needed for different environments.

The line

```dockerfile
CMD python3 /home/gpioByMQTT.py -d False -p "MBR/automation/shutters" -j "shutterConfiguration.json"
```

runs [gpioByMQTT.py](gpioByMQTT.py) given a specific topic and conifguration. MQTT-Settings are left default. 

```py
parser.add_argument('-S','--SERVER', metavar='path', required=False, default="0.0.0.0",help='the mqtt server to publish')
parser.add_argument('-P','--PORT', metavar='path', required=False,default=1883, help='the port to publish to')
parser.add_argument('-p','--path', metavar='path', required=True, help='the mqttt path to publish')
parser.add_argument('-d','--dryrun', metavar='path', required=False, default=True, help='set to False to run in production mode')
parser.add_argument('-j','--jsonconfig', metavar='path', required=True, default=True, help='the path to the pin configuration file')    
```

> It's mandatory to build the image directly on Raspberry Pi to ensure it is working on that architecture. The build command itself can be performed as usually in the folder where the Dockerfile is located.


### [docker-compose.yml]()

For ensuring availability of the host-raspberrypi pins 
its neccessary to give privileged access:

```yaml
volumes:
     - /dev/gpiomem
    privileged: true
```
For secure access to mqtt-password an docker-compose secret is used. 

## Sources

- <https://stackoverflow.com/questions/53094979/how-to-enable-wiringpi-gpio-control-inside-a-docker-container>
- <https://stackoverflow.com/questions/30059784/docker-access-to-raspberry-pi-gpio-pins>
- <https://docs.docker.com/compose/use-secrets/>


