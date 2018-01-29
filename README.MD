# Introduce

A monitor data pusher for shadowsocks/v2ray.

# Usage

## Create config file

    shell> mv config.json.example config.json
    shell> vi config.json

## Start in console

    shell> python3 monitor.py

## Or start by docker

    shell> docker build -t apusher .
    shell> docker run -i -t apusher

## Requirement ##

- Python >=3.4
  - requests
- libsodium
