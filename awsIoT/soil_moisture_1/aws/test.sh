# run pub/sub sample app using certificates downloaded in package
printf "\nRunning pub/sub sample application...\n"
python aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py -e a1f7wlp3u17m26-ats.iot.us-east-1.amazonaws.com -r root-CA.crt -c soil_moisture_1.cert.pem -k soil_moisture_1.private.key
