FROM python:latest

WORKDIR /usr/src/app
COPY . .

RUN ls -la
RUN chmod +x ./start.sh
RUN /bin/bash ./start.sh

CMD python run.py