FROM python:3.8

WORKDIR /home

RUN pip install RPi.GPIO
ADD shutterConfiguration.json /home
ADD gpioByJson.py /home
