# IoT Events
The _iot_events_ directory contains the json-files of all IoT Events.

## ControlPanelInput
This file is the input for the control panel if there is more than one bed.
Its attributes are the thresholds for the appropriate beds

## RainBarrelSensorInput
Contains the value of the rain barrel sensor. Value is the actual fill level.

##SoilMoistureInput
Contains the value of the soil moisture sensor.

## SoilMoistureLogic
Event model for AWS IoT Events. Is checking for soil moisture. Either it is dry, then the watering has
to be activated or it is normal, then nothing happens. To check this, an average of both
soil moisture sensors gets calculated. If it is under 50% nFK the soil is dry.

## WaterSourceDetectorModel
Event model for AWS IoT Events. Decides wether to take water from the rain barrel or the normal
water pipe. If there is more than 10% fill level left in the barrel it is used, 
otherwise it takes the water pipe. 
