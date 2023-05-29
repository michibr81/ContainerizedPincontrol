FROM python:3.8

WORKDIR /home

RUN pip install RPi.GPIO
RUN pip install paho-mqtt

ADD shutterConfiguration.json /home
ADD gpioByJson.py /home
ADD gpioByMQTT.py /home


CMD dir
CMD python3 /home/gpioByMQTT.py dry dry
#ADD gpioByJson.py /home
