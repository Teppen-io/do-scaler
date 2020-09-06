# do-scaler

Autoscales DigitalOcean droplets based on their metrics

* [Introduction](#introduction)
* [Client Configuration](#client-configuration)
* [Server Installation](#server-installation)
  * [Run as a service](#run-as-a-service)
* [Server Configuration](#configuration)
  * [Base Configuration](#base-configuration)
  * [Scaler Configuration](#scaler-configuration)

## Introduction

`do-scaler` runs on a server somewhere and queries droplet metrics that are exposed by the standard `do-agent` monitoring service. (Installed by default on all DigitalOcean droplets.)

Based on your confiuration parameters, it will then create or destroy droplets by leveraging the DigitalOcean API.  Additionally, you can configure your own custom [actions](conf.d/actions).  Some basic actions have been included to get you started.

## Client Configuration

For each droplet that you want to autoscale, you only need to slightly tweak the `do-agent` systemd configuration to expose it's metrics to the autoscaler.  Below you can see that `do-agent` is being configured to expose metrics on the private ipv4 address.

On Ubuntu 18, the `do-agent` systemd configuration lives at: `/etc/systemd/system/do-agent.service`

```
[Unit]
Description=The DigitalOcean Monitoring Agent
After=network-online.target
Wants=network-online.target

[Service]
User=do-agent
ExecStartPre=/bin/sh -c "IP=$(curl -s http://169.254.169.254/metadata/v1/interfaces/private/0/ipv4/address)"
ExecStart=/opt/digitalocean/bin/do-agent --syslog --web.listen --web.listen-address="${IP}:9110"
Restart=always

OOMScoreAdjust=-900
SyslogIdentifier=DigitalOceanAgent
PrivateTmp=yes
ProtectSystem=full
ProtectHome=yes
NoNewPrivileges=yes

[Install]
WantedBy=multi-user.target
```

## Server Installation

```shell
wget https://github.com/Teppen-io/do-scaler/archive/master.zip && \
unzip master.zip && mv do-scaler-master /etc/do-scaler
```

### Run as a service

Create a systemd service config `/etc/systemd/system/do-scaler.service`:

```ini
[Unit]
Description=do-scaler Service

[Install]
WantedBy=default.target

[Service]
Environment=PYTHONUNBUFFERED=1
User=root
ExecStart=/etc/do-scaler/do-scaler/scheduler.py
Restart=on-failure
```

Enable the service:

```shell
systemctl enable do-scaler.service
systemctl start do-scaler.service
```

**Credit:** Florian Brucker [torfsen/python-systemd-tutorial](https://github.com/torfsen/python-systemd-tutorial)

## Server Configuration

### Base Configuration

The `do-scaler` base configuration is implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and is generally stored in `./do-scaler.cfg`

It contains only one configuration directive, `interval` which controls how often the autoscaler runs each of the [Scaler Configurations](#scaler-configuration).

### Scaler Configuration

Scaler configurations are implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and are generally stored in `./conf.d/`

See: [Scaler Configuration](conf.d/)

