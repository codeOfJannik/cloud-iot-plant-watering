FROM python:latest

WORKDIR /usr/src/app
COPY ../../devices/emulator-chronos/chronos_iot .

RUN ls -la
RUN chmod +x ./start.sh
RUN /bin/bash ./start.sh

CMD python run.py