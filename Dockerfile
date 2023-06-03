FROM python:3.8

WORKDIR /home

RUN pip install RPi.GPIO
RUN pip install paho-mqtt

ADD shutterConfiguration.json /home
ADD gpioByMQTT.py /home
ADD gpioByJson.py /home


CMD dir
CMD python3 /home/gpioByMQTT.py
#ADD gpioByJson.py /home
