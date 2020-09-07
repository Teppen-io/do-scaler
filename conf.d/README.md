# do-scaler Scaler Configuration

* [Introduction](#introduction)
* [Example Configuration](#example-configuration)
* [Configuration Options](#configuration-options)
  * [scaler](#scaler)
  * [scaler.metrics](#scaler\.metrics)
  * [<action name>](#action)

## Introduction

A scaler configuration contains all the information needed autoscale a specific droplet based on its tag.  In the config file, you will find a list of the [Policies](./policies) that define thresholds of when to scale up/down, along with the actions that the scaler will perform.

You may have multiple scaler configurations which will all be run on the same interval specified in the [Base Configuration](../README.md#base-configuration).

Scaler Configurations are implemented using [Python Config Parser](https://docs.python.org/3/library/configparser.html) and are stored in `./conf.d/*.cfg`.

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

### scaler ###

#### do_token ####

An API token with Read, Write to your DigitalOcean environment. See: [https://cloud.digitalocean.com/account/api/tokens](https://cloud.digitalocean.com/account/api/tokens)

#### tag_name ####

The tag that is placed on the droplet that you want to autoscale.

#### policy_files ####

A list of json files that define the thresholds of when to scale up/down, along with the actions that the scaler will perform.

See: [Policies](./policies)

### scaler.metrics ###

#### address ####

One of `private_ip_address` or `public_ip_address`.  The scaler will query the droplet's metrcis using this address.

#### port ####

The port on which the droplet has exposed it's metrics.  Should match the [Client Configuration](../README.md#client-configuration).

### action ###

The configuration needed by each of the actions defined in your policy files.  It will vary depending on the requrirements of that specific action.

The config section should be named the same as the action.

For more see: [Actions](./actions)
