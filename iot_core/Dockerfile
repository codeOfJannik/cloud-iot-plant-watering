FROM python:latest

WORKDIR /usr/src/cert

RUN curl https://www.amazontrust.com/repository/AmazonRootCA1.pem > root-CA.crt
RUN pip install AWSIoTPythonSDK
RUN pip install pyyaml
RUN ls -la

WORKDIR ../software

COPY software_class /usr/src/software/software_class/
COPY run.py /usr/src/software/run.py

RUN ls -la

CMD python run.py
