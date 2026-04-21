sops exec-env .env 'esphome -s wifi_ssid "$wifi_ssid" -s wifi_password "$wifi_password" compile cyd-immich-memories.yaml' 
