# JVC DILA for Home Assistant

## Installation
1) copy the folder under config/custom_components
2) restart Home Assistant
3) add sensor and binary sensor in config.yaml
sensor:
  - platform: jvc_dila
    name: <optional name>
    host: <ip address of the projector>
    port: <port of the projector, default is 20554>
    scan_interval: <must be bigger than 1 as that is the tcp timeout.>

binary_sensor:
  - platform: jvc_dila
    name: <optional name>
    host: <ip address of the projector>
    port: <port of the projector, default is 20554>
    scan_interval: <must be bigger than 1 as that is the tcp timeout.>
