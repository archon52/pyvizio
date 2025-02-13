## Description

Simple cli and API implementation for Vizio SmartCast TVs and Sound Bars. Mainly created for 
integration with [HASS](http://home-assistant.io). Note that some of the interaction commands are not supported by 
sound bars.

## Installation

Either through pip

```
pip3 install git+https://github.com/vkorn/pyvizio.git@master
```

or checkout repo and run 

```
pip3 install -I .
```

## CLI Usage

To avoid repeating IP (`--ip`), Auth (`--auth`), and Device Type (`--device_type`) params in each CLI call, you can add them to environment variables as `VIZIO_IP`, `VIZIO_AUTH`, and `VIZIO_DEVICE_TYPE` respectively

`--device-type` options are `tv` and `soundbar`. If the parameter is not included, the device type is assumed to be `tv`. Note that TVs always require a pairing process to get an auth token. Sound Bars may not always need an auth token but YMMV based on your particular model.

### Find your device

First, find your device (yeah, I'm too lazy to add another cli group)
```
pyvizio --ip=0 discover
```

and note it's IP address. If using your IP address by itself does not lead to success, you may need to append `:9000` or `:7345` to it when using it as a parameter in future commands. 

### Pairing

> For a Sounnd Bar, it is unclear how the device would notify you of a valid auth token, so it's best to first skip the pairing process entirely, specify `--device_type=soundbar`, and try commands like `volume-current` to see if you have any success. If not, and if specifying different ports as mentioned above doesn't work, you will need to find a way to get the auth token during this process.

Using your device's IP address, request pairing procedure:

```
pyvizio --ip={ip} --device_type={device_type} pair
```

For TVs, lookup the PIN code on your TV, and note challenge token in console. It's not clear how you would obtain an auth token for a Sound Bar. 

> Better to have device turned on as it's "forgetting" PIN sometimes if it was 
turned off prior to pairing command

Using these dafa finalize pairing procedure
```
pyvizio --ip={ip} --device_type={device_type} pair-finish --token={challenge_token} --pin={_pin} 
```
If everything done correctly, you should see new connected device named `Python Vizio` 
in Vizio SmartCast mobile APP 


> For a TV, you'll need auth code for any further commands. If you are interacting with a Sound Bar, and skipped the pairing process, you don't need to include the `--auth` parameter in any of the following calls since you don't have an auth code.

### Turning on/off

```
pyvizio --ip={ip} --device_type={device_type} --auth={auth_code} power {on|off|toggle}
```

To get current power state simply call

```
pyvizio --ip={ip} --device_type={device_type} --auth={auth_code} power-get
``` 

### Volume operations

You could change volume

```
pyvizio --ip={ip} --device_type={device_type} --auth={auth_code} volume {up|down} amount
```

and get current level (0-100)

```
pyvizio --ip={ip} --device_type={device_type} --auth={auth_code} volume-current
```

In addition mute command is available

```
pyvizio --ip={ip} --device_type={device_type} --auth={auth_code} mute {on|off|toggle}
```

### Switching channels
```
pyvizio --ip={ip} --device_type={device_type} --auth={auth_code} channel {up|down|prev} amount
```

### Input sources

You can get current source 

```
pyvizio --ip={ip} --device_type={device_type} --auth={auth_code} input-get
```

List all connected devices

```
pyvizio --ip={ip} --device_type={device_type} --auth={auth_code} input-list
```

And using `Name` column from this list, you can switch input:

```
pyvizio --ip={ip}  --device_type={device_type} --auth={auth_code} input --name={name}
```

Other options is to circle through all inputs
```
pyvizio --ip={ip} --device_type={device_type} --auth={auth_code} input-next
``` 

## Contribution

Thanks for great research uploaded [here](https://github.com/exiva/Vizio_SmartCast_API) and 
absolutely awesome SSDP discovery [snippet](https://gist.github.com/dankrause/6000248)
