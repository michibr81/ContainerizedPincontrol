# ContainerizedPincontrol

This project aims to get the RaspBerryPi pin control python library [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) running in an Docker Container.

## Configuration

- [Dockerfile](Dockerfile)

The image is based on `python` and the important parts are


```docker
FROM python:3.8

WORKDIR /home

RUN pip install RPi.GPIO
ADD dataReworked.json /home
ADD gpioByJson.py /home
```

The files *dataReworked.json* and *gpioByJson.py* are needed for the pin-actions performed in my case so there is no magic in there. Any other python script using [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) can be added to the image.

### Building image

It's mandatory to build the image directly on Raspberry Pi to ensure it is working on that architecture. The build command itself can be performed as usually in the folder where the Dockerfile is located.

```bash
docker build "." -t pincontrol
```

### Running the container

To ensure access to pincontrol, docker container must be run as follows:

```bash
sudo docker run --device /dev/gpiomem -it pintestimage bash
```
The `-it` parameter just gives bash access in the running container. Other options may be more reasonable for running in production.

Sources:
- <https://stackoverflow.com/questions/53094979/how-to-enable-wiringpi-gpio-control-inside-a-docker-container>
- <https://stackoverflow.com/questions/30059784/docker-access-to-raspberry-pi-gpio-pins>


