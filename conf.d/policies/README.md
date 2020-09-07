# do-scaler Policy Configuration

* [Introduction](#introduction)
* [Configuration Options](#configuration-options)
  * [name](#name)
  * [actions](#actions)
  * [match](#match)
  * [conditions](#conditions)
    * [name](#name-1)
    * [reducer](#reducer)
    * [samples](#samples)
      * [name](#name-2)
      * [family](#family)
    * [operator](#operator)
    * [threshold](#threshold)
    * [function](#function)

## Introduction

Policies define conditions and thresholds that dictate when to scale up/down.  They are written in json and are stored in `./conf.d/policies/*.json`

## Configuration Options

### name ###

The policy's name.

### actions ###

A list of actions to perform if the required conditions are met.

See: [Actions](../actions)

### match ###

One of `any`, `all`.  Either `any` of the conditions need to be met before perfoming the actions, or `all` of them.

### conditions ###

A list of conditions to match.

#### name ####

The name of the condition.

#### reducer ####

One of `+`, `-`, `*`, `/`.   If defining multiple metric samples, you can reduce them down to one using these symbols.

For an example see: [down.json](down.json#L8-L24) where `node_memory_MemFree_bytes` and `node_memory_Cached_bytes` are summed to create `mem_avail`.

#### samples ####

##### name #####

The name of the metric sample.

##### family #####

The family of the metric sample.

#### operator ####

One of `<`, `<=`, `>`, `>=`, `==`.  Used to compare the metric sample against the threshold.

#### threshold ####

The threshold used to compare against the metric sample.

#### function ####

One of `min`, `max`, `median`, `mean`.  When querying a group of droplets for their metrics these functions are used to determine which value to use to compare against the threshold.
