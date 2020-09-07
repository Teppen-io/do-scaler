# do-scaler Actions

* [Introduction](#introduction)
* [Configuration Options](#configuration-options)
* [Custom Actions](#custom-actions)

## Introduction ##

Actions are standard Python classes that are stored in `./conf.d/actions/`.

## Configurtion Options ##

Actions have their config passed to them by the scaler.  The config is defined in the same file as the standard [Scaler Configuration](../).

The config section should be named the same as the action.

## Custom Actions ##

Three basic actions have been included for you, however you can create your own Python Classes to perform whatever logic you want.  They will be dynamically loaded at runtime by the scaler.

Actions must have a `run` method that will be called by the scaler after the conditions defined in the policy have been met.
