# IoT Events
The _iot_events_ directory contains the json-files of all IoT Events.

## ControlPanelInput
This file is the input for the control panel for all beds.
Its attributes are the thresholds for the appropriate beds (in % nFK).

## RainBarrelSensorInput
Contains the value of the rain barrel sensor. Value is the actual fill level (in %).

## SoilMoistureInput
Contains the value of the soil moisture sensor (in % nFK).

## SoilMoistureLogic
Event model for AWS IoT Events. Is checking for soil moisture. Either it is dry, then the watering has
to be activated or it is normal, then the watering has to be deactivated. To check this, an _'moving'_ average of all
soil moisture sensors gets calculated. If it is under the set value in the control panel (default 50% nFK), the soil is 
dry.

## WaterSourceDetectorModel
Event model for AWS IoT Events. Decides wether to take water from the rain barrel or the normal
water pipe. If there is more than 10% fill level left in the barrel it is used, 
otherwise it takes the water pipe. Here it can be a future work to set the fill level by the control panel.
