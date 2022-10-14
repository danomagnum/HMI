# HMI

A python based HMI system.  You can define your devices in the config/drivers.json file and then read/write from each device with the /read/driver/tag and /write/driver/tag apis.

![Screenshot](https://github.com/danomagnum/HMI/blob/main/screenshots/Screenshot_2022-10-14_11-35-37.png)


Screens are jinja hmtl templates were elements with specific classes set get turned into HMI elements.

the `autoload_value` class signals the system to read the `data-target` property and update the value property if it has one, otherwise it will replace the innerhtml.

Here is an example of a multistate indicator like you'd find in other packages:
```
<select class="autoload_value multistate_indicator" data-target="plc/Program:Smoker.state" value="false">
		<option value="0">Off</option>
		<option value="10">Purge</option>
		<option value="20">Ignite</option>
		<option value="30">Ramp Up</option>
		<option value="40">PID Hold</option>
		<option value="50">Ramp Down</option>
		<option value="100">Shutdown</option>
	</select>
```

Here's a data input box.  Inputs with the `autooad_value` class will automatically write to their `data-target` when updated.
```
<span class="label">Burner SP</span>
	<input class="autoload_value" data-target="plc/Program:Smoker.temp_sp", value=0>
```

Here's a button.  Buttons use the special classes `pb_momentary` and `pb_toggle` with `data-press` and `data-release` properties.:
```
<button class="pb_toggle" data-target="plc/Program:Smoker.enable_autostart" data-press="1" data-release="0">Autostart</button>
```


New drivers can be added to the drivers directory.  The CIP driver uses pylogix to communicate to allen bradley PLCs.  There is also a modbus driver but I don't remember if I ever tested it so it might or might not work.  There is also a "driver" that will execute simple ladder logic and there is a driver for "internal" hmi tags.
