# Dweet.io to MQTT Integration

The format of a dweeted command is `<action> <data1> <data2> ... <dataN>`

Based on the default configuration found in [config.py](config.py), the following commands are available and will be recognised by the Tree MQTT Service found in the folder [../tree_mqtt_service](../tree_mqtt_service)


## Clear (turn off) all LEDS on APA102 LED Strip

`clear`

*Example:*

`https://dweet.io/dweet/for/<thing_name>?command=clear`

*Mapping:*

This command is mapped into:

  * Action `clear` is mapped to MQTT Topic `tree/lights/clear`
  * There is no data. An empty MQTT message is used. 

An equivalent `mosquitto_pub` example would be:

`mosquitto_pub -h "localhost" -t "tree/lights/clear" -m ""`

---

## Push color(s) into the APA102 LED Strip

`push <color1> <color2> <colorN>`

The `color` parameters are name like red or green, or a hex value like #FF0033

*Example:*

`https://dweet.io/dweet/for/<thing_name>?command=push%20red%20blue%20black`

*Mapping:*

This command is mapped into:

  * Action `push` is mapped to MQTT Topic `tree/lights/push`
  * Data `red blue back` becomes MQTT Message `red blue black`

An equivalent `mosquitto_pub` example would be:

`mosquitto_pub -h "localhost" -t "tree/lights/push" -m "red blue black"`

---

## Set Repeating Color Pattern on the APA102 LED Strip

`pattern <color1> <color2> <colorN>`

The `color` parameters are name like red or green, or a hex value like #FF0033

*Example:*

`https://dweet.io/dweet/for/<thing_name>?command=pattern%20red%20blue%20black`

*Mapping:*

This command is mapped into:

  * Action `pattern` is mapped to MQTT Topic `tree/lights/pattern`
  * Data `red blue back` becomes MQTT Message `red blue black`

An equivalent `mosquitto_pub` example would be:

`mosquitto_pub -h "localhost" -t "tree/lights/pattern" -m "red blue black"`

---

## Set LED Contrast

`contrast <level>`

The `level` parameter expects a value between `0` and `255`.

*Example:*

`https://dweet.io/dweet/for/<thing_name>?command=contrast%20128`

*Mapping:*

This command is mapped into:

  * Action `contrast` is mapped to MQTT Topic `tree/lights/contrast`
  * Data `128` becomes MQTT Message `128`

An equivalent `mosquitto_pub` example would be:

`mosquitto_pub -h "localhost" -t "tree/lights/contrast" -m "128"`

---

## Set LED Animation Mode

`animation <mode>`

The `mode` parameter expects one of the following values:

  * stop
  * left
  * right
  * blink
  * rainbow

*Example:*

`https://dweet.io/dweet/for/<thing_name>?command=animation%20left`

*Mapping:*

This command is mapped into:

  * Action `animation` is mapped to MQTT Topic `tree/lights/animation`
  * Data `left` becomes MQTT Message `left`

An equivalent `mosquitto_pub` example would be:

`mosquitto_pub -h "localhost" -t "tree/lights/animation" -m "left"`

---

## Set LED Animation Speed

`speed <speed>`

The `speed` parameter expects a value between `1` and `10`.

*Example:*

`https://dweet.io/dweet/for/<thing_name>?command=speed%2010`

*Mapping:*

This command is mapped into:

  * Action `speed` is mapped to MQTT Topic `tree/lights/speed`
  * Data `10` becomes MQTT Message `10`

An equivalent `mosquitto_pub` example would be:

`mosquitto_pub -h "localhost" -t "tree/lights/speed" -m "10"`

---

## Sweep the Servo

`sweep`

*Example:*

`https://dweet.io/dweet/for/<thing_name>?command=sweep`

*Mapping:*

This command is mapped into:

  * Action `sweep` is mapped to MQTT Topic `tree/servo/sweep`
  * There is no data. An empty MQTT message is used. 

An equivalent `mosquitto_pub` example would be:

`mosquitto_pub -h "localhost" -t "tree/servo/sweep" -m ""`
