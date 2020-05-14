FROM python:latest

WORKDIR /files/aws
COPY /aws .

RUN chmod +x start.sh
RUN /bin/bash ./start.sh

RUN chmod +x test.sh
CMD ./test.sh
