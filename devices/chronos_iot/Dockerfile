FROM python:latest

WORKDIR /usr/src/cert

RUN curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt
RUN pip install AWSIoTPythonSDK
RUN ls -la

CMD python ../app/run.py