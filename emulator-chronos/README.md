# Hardware Emulator

Hardware emulator with REST interface for GPIOs

<img alt="Screenshot of Web UI" src="https://gitlab.mi.hdm-stuttgart.de/csiot/emulator/-/raw/master/assets/screenshot.png" height="250px">

- Emulates a physical IoT device, such as a Raspberry Pi, Arduino, ESP, ...
- Implementation of the device software is up to you
- Reads an emulator config with GPIOs from ``/emulator/config.yaml``
- Starts a webserver with a web UI and a REST interface at port ``9292``

## Install

The ``./build`` command builds a ``csiot/emulator`` image you can include into any docker stack.
Please run it insude the emulator folder.

## Use in Project

In a ``docker-compose.yaml`` stack you can use this image to replace the physical hardware device, e.g.:

```yaml
version: "3"
services:

  # hardware emulation starts a server for you on port 9292
  sensor_emulator:
    image: csiot/emulator
    ports:
      - "127.0.0.1:3333:9292"
    volumes:
      - "./config.yaml:/emulator/config.yaml"
  
  # software implementation is up to you, connect to hardware via sensor_emulator:9292
  sensor_software:
    image: python
```

Now you can visit ``http://localhost:3333`` in your browser.

Note: A full IoT device always consists of an emulator and a software service!

## Config

The ``config.yaml`` defines what components are in your emulator.
Components can be accessed via GPIOs - just like with real hardware.

You can start from the sample config in this repo, where the following outputs and inputs are available.

### LED

Visual led that can be turned on and off.

```yaml
name: LED Device
gpios:

  led_green:
    type: led
    state:
      # by default this is off
      'on': false
      
      # color can be any named css color value
      color: green
	
  led_red:
    type: led
    state:
      # by default this is on
      'on': false
      
      # color can be any css color value
      color: '#f44336'
```

Read the current LED value:

``curl -s localhost:3333/gpios/led_green | jq``

```json
{
  "id": "led_green",
  "type": "led",
  "direction": "output",
  "state": {
    "on": false,
    "color": "green"
  }
}
```

Set the current LED value:

``curl -s -d '{ "on": true }' localhost:3333/gpios/led_green | jq``

```json
{
  "id": "led_green",
  "type": "led",
  "direction": "output",
  "state": {
    "on": true,
    "color": "green"
  }
}
```

### Switch

Hardware switch that can be open or closed.

```yaml
name: Switch Device
gpios:
  power_switch:
    type: switch
    state:
      open: false
```

Read the current switch value:

``curl -s localhost:3333/gpios/power_switch | jq``

```json
{
  "id": "power_switch",
  "type": "switch",
  "direction": "input",
  "state": {
    "open": false
  }
}
```

Change the current switch value:

``curl -s -d '{ "open": true }' localhost:3333/gpios/power_switch | jq``

```json
{
  "id": "power_switch",
  "type": "switch",
  "direction": "input",
  "state": {
    "open": true
  }
}
```

### Sensor

Hardware sensor that can measure values in a predefined range:

```yaml
name: Sensor Device
gpios:
  temp_sensor:
    type: sensor
    state:
      # the initial value
      value: 21
      
      # the minimal value
      min: 15
      
      # the maximum value
      max: 30
      
      # the step-size if the value goes up or down
      increment: 1
      
      # the unit (UI only, empty string for unitless)
      unit: "C"
```

Read the current sensor value:

``curl -s localhost:3333/gpios/temp_sensor | jq``

```json
{
  "id": "temp_sensor",
  "type": "sensor",
  "direction": "input",
  "state": {
    "value": 21,
    "min": 15,
    "max": 30,
    "increment": 1,
    "unit": "C"
  }
}
```

Change the current sensor value (usually only used from UI):

``curl -s -d '{ "value": 28 }' localhost:3333/gpios/temp_sensor | jq``

```json
{
  "id": "temp_sensor",
  "type": "sensor",
  "direction": "input",
  "state": {
    "value": 28,
    "min": 15,
    "max": 30,
    "increment": 1,
    "unit": "C"
  }
}
```

## REST API


### GET /gpios

Get all GPIOs:

``curl -s localhost:3333/gpios | jq``

```json
{
  "led_green": {
    "id": "led_green",
    "type": "led",
    "direction": "output",
    "state": {
      "on": true,
      "color": "green"
    }
  },
  "led_red": {
    "id": "led_red",
    "type": "led",
    "direction": "output",
    "state": {
      "on": false,
      "color": "#f44336"
    }
  },
  "temp_sensor": {
    "id": "temp_sensor",
    "type": "sensor",
    "direction": "input",
    "state": {
      "value": 28,
      "min": 15,
      "max": 30,
      "increment": 1,
      "unit": "C"
    }
  },
  "power_switch": {
    "id": "power_switch",
    "type": "switch",
    "direction": "input",
    "state": {
      "open": false
    }
  }
}
```

### GET+POST /gpios/:id

Get and set GPIO by id

``curl -s localhost:3333/gpios/led_green | jq``

```json
{
  "id": "led_green",
  "type": "led",
  "direction": "output",
  "state": {
    "on": false,
    "color": "green"
  }
}
```

``curl -s -d '{ "on": true }' localhost:3333/gpios/led_green | jq``

```json
{
  "id": "led_green",
  "type": "led",
  "direction": "output",
  "state": {
    "on": true,
    "color": "green"
  }
}
```

### GET /device

Get full device info

``curl -s localhost:3333/device | jq``

```json
{
  "name": "Default Device",
  "gpios": {
    "led_green": {
      "id": "led_green",
      "type": "led",
      "direction": "output",
      "state": {
        "on": true,
        "color": "green"
      }
    },
    "led_red": {
      "id": "led_red",
      "type": "led",
      "direction": "output",
      "state": {
        "on": false,
        "color": "#f44336"
      }
    },
    "temp_sensor": {
      "id": "temp_sensor",
      "type": "sensor",
      "direction": "input",
      "state": {
        "value": 28,
        "min": 15,
        "max": 30,
        "increment": 1,
        "unit": "C"
      }
    },
    "power_switch": {
      "id": "power_switch",
      "type": "switch",
      "direction": "input",
      "state": {
        "open": false
      }
    }
  }
}
```

## Examples

Have a look into the ``example`` folder.
