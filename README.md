# JVC DILA sensor for Home Assistant

WARNING: if you configure both the BinarySensor and the Sensor you'll get errors. Use one of them.
Working on a new version to solve it

## Installation

### MANUAL INSTALLATION
1. Download the
   [latest release](https://github.com/msavazzi/homeassistant-jvc-dila/releases/tag/tcp_based).
2. Unpack the release and copy the `custom_components/jvc_dila` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Add configuration in config.yaml
5. Restart Home Assistant.

## Configuration

To add a variable, include it under the `sensor` and `binary_sensor` sections in your
`configuration.yaml`. 

```yaml
# Example configuration.yaml entry
sensor:
  - platform: jvc_dila
    host: 192.168.1.2
    port: 20554
    scan_interval: 10

binary_sensor:
  - platform: jvc_dila
    host: 192.168.1.2
    port: 20554
    scan_interval: 10
```

### CONFIGURATION VARIABLES

* **name**
  *(string)(Optional)*
  Name to use in the frontend.
* **host**
  *(string)(Required)*
  ip address of the projector
* **port**
  *(int)(Required)*
  port of the projector, default is 20554
* **scan_interval**
  *(int)(Optional)*
  Number of seconds between queries to the projector
  must be bigger than 8 due to the internal timeouts the JVC DILA Projector requires.

## Why?

I want to have the status of the projector to trigger actions
