# IoTree API Service


## GET IoTree State

### GET /lights

Get full state server state APA102 LED Strip.

*Example:*

`curl -X GET "http://localhost:5000/lights"`

*Response:*

```
{
    "success": true,
    "state": {
        "contrast": 128,
        "animation": "off",
        "speed": 5,
        "colors": [
            "black",
            "blue",
            "red"
        ]
    }
}
```

*Implementation:*

See `StateControl.get()` in file `apa102_api.py`

---

## Clear (turn off) all LEDS on APA102 LED Strip

### POST /lights/clear

Clear APA102 LED Strip.

*Example:*

`curl -X POST "http://localhost:5000/lights/clear"`

*Response:*

```
{
    "success": true
}
```

*Implementation:*

See `ClearControl.post()` in file `apa102_api.py`

---

## Push color(s) into the APA102 LED Strip

### GET /lights/color

Get current color sequence.

*Example:*

`curl -X GET "http://localhost:5000/lights/color"`

*Response:*

```
{
    "success": true,
    "state": {
        "colors": [
            "black",
            "blue",
            "red"
        ]
    }
}
```

*Implementation:*

See `ColorControl.get()` in file `apa102_api.py`

---

## Set Repeating Color Pattern on the APA102 LED Strip

### POST /lights/color?colors=color1,color1,colorN,pattern=yes|no

Set colors on the APA102 LED Strip. If `pattern=no`, colors are pushed into the LED Strip. When `pattern=y` colours are applied as a repeating color pattern.

*Example:*

`curl -X POST "http://localhost:5000/lights/color?colors=red,blue,black&pattern=no"`

*Response:*

```
{
    "success": true,
    "state": {
        "colors": [
            "black",
            "blue",
            "red"
        ]
    }
}
```

*Implementation:*

See `ColorControl.post()` in file `apa102_api.py`

---

## Get LED Contrast

### GET /lights/contrast

Get LED contrast level.

*Example:*

`curl -X GET "http://localhost:5000/lights/contrast"`

*Response:*

```
{
    "success": true,
    "state": {
        "contrast": 128
    }
}
```

*Implementation:*

See `ContrastControl.get()` in file `apa102_api.py`

---

## Set LED Contrast

### POST /lights/contrast?level=0..255

Set LED contrast. Parameter `level` expects a value between `0` (off) and `255` (full contrast).

*Example:*

`curl -X POST "http://localhost:5000/lights/contrast?level=128"`

*Response:*

```
{
    "success": true,
    "state": {
        "contrast": 128
    }
}
```

*Implementation:*

See `ContrastControl.post()` in file `apa102_api.py`

---

## Get LED Animation Mode

### GET /lights/animation

Get current animation

*Example:*

`curl -X GET "http://localhost:5000/lights/animation"`

*Response:*

```
{
    "success": true,
    "state": {
        "animation": "blink",
        "speed": 5
    }
}
```

*Implementation:*

See `AnimationControl.post()` in file `apa102_api.py`

---

## Set LED Animation Mode & Speed

### POST /lights/animation?mode=stop|left|right|blink|rainbow&speed=1..10

Start or stop light animation.

 * Parameter `mode` sets the animation mode, and expects a value of `stop`, `left`, `right`, `blink`, or `rainbow`
 * Parameter `speed` sets the animation speed between `1` (slowest) and `10` (fastest). 

*Example:*

`curl -X POST "http://localhost:5000/lights/animation?mode=blink&speed=5"`

*Response:*

```
{
    "success": true,
    "state": {
        "animation": "blink",
        "speed": 5
    }
}
```
*Implementation:*

See `AnimationControl.post()` in file `apa102_api.py`

---

## Sweep the Servo

### POST /servo/sweep

Makes the Servo _sweep_.
 
*Example:*

`curl -X POST "http://localhost:5000/servo/sweep"`

*Response:*
```
{
    "success": true
}
```

*Implementation:*

See `SweepControl.post()` in file `servo_api.py`

