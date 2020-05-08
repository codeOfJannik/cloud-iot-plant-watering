# Notes

## Questions
- [ ] CICD: Gitlab or Cloud (Jenkins)?
- [ ] Sensor query: by Cloud request or Controler loop?
> To run all major logic in the cloud seems to be the better approach. A short example why:
> We got multiple controllers with a lot of sensors. Each controller runs its 
> own loop to query sensor data and sends it to the cloud.
>
> 1. Not all sensor data is saved to the same entry in a time series database, cause
> there may be differences between the timestamps of the responses of different
> controllers. If the data is queried by a request from the cloud, all data of
> the controller responses can be associated with the timestamp of the global query.
>
> 2. If one controller is restarted after it ran out of battery, the loop of
> this controller wouldn't be synced with the other controllers. But if the
> sensor data is queried by the cloud, the response of all controllers will
> always be synced.
> 
> Update:
> AWS IoT seems to have no possibility to trigger data queries. As you can
> see [here](https://docs.aws.amazon.com/de_de/iot/latest/developerguide/iot-moisture-raspi-setup.html),
> the RaspberryPi has a loop that reads the data of the sensors and updates the
> AWS IoT shadow.
