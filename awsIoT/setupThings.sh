#!/bin/sh
if [ "$#" -ne 2 ]; then
	echo 'Invalid number of arguments passed. Require 2 arguments (./setupThings.sh sensorname endpoint)'
	exit 1
fi

SENSOR_NAME=$1
AWS_ENDPOINT=$2

echo "Create directory ${SENSOR_NAME}"
mkdir $SENSOR_NAME
cp ./setupThing.tf ./$SENSOR_NAME/
cd $SENSOR_NAME

echo "Start terraform init"
terraform init

echo "Start terraform script for setup of ${SENSOR_NAME}"

terraform apply -var="sensor_name=${SENSOR_NAME}"
echo 'Finished terraform apply'

echo 'Create directory /aws'
mkdir aws

echo 'Move certificate and private key to directory /aws'
mv ./$SENSOR_NAME.cert.pem aws/
mv ./$SENSOR_NAME.private.key aws/
cp ../start.sh aws/

echo 'Create test.sh script'
touch aws/test.sh
echo '# run pub/sub sample app using certificates downloaded in package' >> aws/test.sh
echo 'printf "\nRunning pub/sub sample application...\n"' >> aws/test.sh
echo "python aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py -e ${AWS_ENDPOINT} -r root-CA.crt -c ${SENSOR_NAME}.cert.pem -k ${SENSOR_NAME}.private.key" >> aws/test.sh

echo 'execute docker build'
docker build -t "${SENSOR_NAME}_image" -f ../Dockerfile .

