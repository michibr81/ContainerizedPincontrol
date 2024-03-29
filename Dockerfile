FROM python:3.8

WORKDIR /home

RUN pip install RPi.GPIO
RUN pip install paho-mqtt

ADD shutterConfiguration.json /home
ADD gpioByMQTT.py /home
ADD gpioByJson.py /home

CMD python3 /home/gpioByMQTT.py -d False -p "MBR/automation/shutters" -j "shutterConfiguration.json"
#ADD gpioByJson.py /home
