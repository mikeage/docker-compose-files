# CYD Monitor ESPHome

Run these commands from this directory.

Edit the encrypted configuration:

```bash
EDITOR=nvim sops edit cyd-monitor.yaml
```

Validate the configuration:

```bash
sops exec-file --filename cyd-monitor.yaml cyd-monitor.yaml 'esphome config {}'
```

Compile the firmware:

```bash
ESPHOME_BUILD_PATH="$PWD/.esphome/build" sops exec-file --filename cyd-monitor.yaml cyd-monitor.yaml 'esphome compile {}'
```

Compile, upload, and follow logs:

```bash
ESPHOME_BUILD_PATH="$PWD/.esphome/build" sops exec-file --filename cyd-monitor.yaml cyd-monitor.yaml 'esphome run {}'
```
