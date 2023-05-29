FROM python:3.8

WORKDIR /var/mqtt

RUN pip install RPi.GPIO
RUN pip install paho-mqtt

ADD shutterConfiguration.json /var/mqtt
ADD gpioByJson.py /var/mqtt
ADD gpioByMQTT.py /var/mqtt

ENTRYPOINT /var/mqtt
RUN python /var/mqtt/gpioByMQTT.py dry dry
