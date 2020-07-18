# IoT Events
The _iot_events_ directory contains the json-files to setup the AWS IoT Event resources via AWS CLI command.

## Detector Models 
### SoilMoistureLogic
AWS IoT Event model for handling of soil moisture and watering of the beds. Either the soil of a bed it is dry, then the watering has
to be activated or it is normal, then the watering has to be deactivated. To check this, a _'moving'_ average of all
soil moisture sensor readings of the bed is calculated. In a time interval, that can be set at two places (` "setTimer": {"timerName": "CheckTimer","seconds": 60})` of the [SoilMoistureLogic.json](SoilMoistureLogic.json), the  _'moving'_ average is compared to the soil moisture threshold set on the control panel for the bed.
After the check the desired state of the belonging watering valve is set via publish on an MQTT topic.

A detector model instance for each bed is created autmatically. The bed_id which is part of the [ControlPanelInput](#controlpanelinput) and the 
[SoilMoistureInput](#soilmoistureinput) is used as key for the detector model.
That means for every input with a unknown bed_id, a new detector model instance is created.
The SoilMositureLogic detector model uses the values of [ControlPanelInput](#controlpanelinput) and [SoilMoistureInput](#soilmoistureinput).

### WaterSourceDetectorModel
AWS IoT Event model to decide whether to take water from the rain barrel or the normal water pipe.
The current fill level of the rain barrel is compared to the minimum fill level set on the control panel. If the current fill level is larger than the
specified minimum fill level, the desired state of the watering source valve is changed via publish to a MQTT topic to use the water from the rain barrel.
If the fill level is smaller, the watering source valve is set to use the water pipe.
The WaterSourceDetectorModel uses the values of [RainBarrelSensorInput](#rainbarrelsensorinput) and [RainBarrelThresholdInput](#rainbarrelthresholdinput)

## Inputs

### ControlPanelInput
Soil mositure threshold specified via control panel and the related _bed_id_. The _bed_id_ is used by the [SoilMositureLogic](#soilmoisturelogic) as key for the detector model instances.
```json
{
    "value": 50,
    "bed_id": 1
}
```


### SoilMoistureInput
Reading (value) of a soil moisture sensor and the _bed_id_ of the bed the sensor is belonging to. Used by the [SoilMositureLogic](#soilmoisturelogic) detector model with _bed_id_ as key.
```json
{
    "value": 45,
    "bed_id": 2
}
```

### RainBarrelSensorInput
Fill level (value) of the rain barrel in %. Used by the [WaterSourceDetectorModel](#watersourcedetectormodel).
```json
{
    "value": 80
}
```


### RainBarrelThresholdInput
Rain barrel threshold specified via control panel. Used by the [WaterSourceDetectorModel](#watersourcedetectormodel).
```json
    "value": 20
```
