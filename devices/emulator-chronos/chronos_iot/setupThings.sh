#!/bin/sh
if [ "$#" -ne 2 ]; then
	echo 'Invalid number of arguments passed. Require 2 arguments (./setupThings.sh sensorname endpoint)'
	exit 1
fi

SENSOR_NAME=$1
AWS_ENDPOINT=$2

echo "Copy terraform script into ${SENSOR_NAME}"
cp ./setupThing.tf ./$SENSOR_NAME/
cp ./start.sh ./$SENSOR_NAME/
cd $SENSOR_NAME

echo "Start terraform init"
terraform init

echo "Start terraform script for setup of ${SENSOR_NAME}"

terraform apply -var="sensor_name=${SENSOR_NAME}"
echo 'Finished terraform apply'

echo 'Create directory /aws_credentials'
mkdir aws_credentials

echo 'Move certificate and private key to directory /aws'
mv ./$SENSOR_NAME.cert.pem aws_credentials/
mv ./$SENSOR_NAME.private.key aws_credentials/

echo 'execute docker build'
# docker build -t "${SENSOR_NAME}_image" -f ../Dockerfile .
cd ../
docker-compose up


