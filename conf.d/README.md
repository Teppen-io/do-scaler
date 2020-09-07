# do-scaler Scaler Configuration

* [Introduction](#introduction)
* [Example Configuration](#example-configuration)
* [Configuration Options](#configuration-options)
  * [scaler](#scaler)
  * [scaler.metrics](#scaler.metrics)
  * [action](#action)

## Introduction

Scaler Configurations are implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and are stored in `./conf.d/*.cfg`

## Example configuration

```
[scaler]
do_token = 00000000000000000000000000000000000000000000000000000000000000000
tag_name = web
policy_files = mem_avail.json loadavg.json down.json

[scaler.metrics]
address = private_ip_address
port = 9110

[digitalocean_create_droplet]
do_token = ${scaler:do_token}
max = 8
droplet = web.json

[digitalocean_destroy_droplet]
min = 2

[health_check_tcp]
address = private_ip_address
ports = 9110 80
timeout = 10
interval = 10
max_tries = 12
```

## Configuration Options

A scaler configuration contains all the information needed autoscale a specific droplet based on its tag.  In the config you will find a list of the [Policies](./policies) that define thresholds of when to scale up/down, along with the configuration for all the actions that the scaler will perform.  You may have multiple scaler configurations which will all be run on the same interval specified in the [Base Configuration](../README.md#base-configuration).

### scaler ###

#### do_token ####

#### tag_name ####

#### policy_files ####

### scaler.metrics ###

#### address ####

#### port ####

### action ###

Defines the configuration needed by each of the actions defined in your policy files.  It will vary depending on the requrirements of that specific action.

For more see: [Actions](./actions)
