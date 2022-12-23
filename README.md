# JVC DILA sensor for Home Assistant

The `var` component is a Home Assistant integration for declaring and

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


### INSTALLATION VIA HACS
1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Search for and install the "Variable" integration.
3. Add a `var` entry to your `configuration.yaml`.
4. Restart Home Assistant.

## Configuration

To add a variable, include it under the `sensor` and `binary_sensor` sections in your
`configuration.yaml`. 

```yaml
# Example configuration.yaml entry
sensor:
  - platform: jvc_dila
    host: 192.168.1.2
    port: 20554
    scan_interval: 3

binary_sensor:
  - platform: jvc_dila
    host: 192.168.1.2
    port: 20554
    scan_interval: 3
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
  must be bigger than 1 as that is the tcp timeout.

## Why?

I want to have the status of the projector to trigger actions
