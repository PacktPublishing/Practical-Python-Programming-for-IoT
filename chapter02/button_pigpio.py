"""
File: chapter02/button_gpiozero.py

Turn on and off an LED with a Button using PiGPIO.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import pigpio
import signal

LED_GPIO_PIN = 21
BUTTON_GPIO_PIN = 23

pi = pigpio.pi()


# LED provides 'Output'
pi.set_mode(LED_GPIO_PIN, pigpio.OUTPUT)
pi.write(LED_GPIO_PIN, 0)  # LED Off


# Button provides 'Input'
pi.set_mode(BUTTON_GPIO_PIN, pigpio.INPUT)                                       # (1)
pi.set_pull_up_down(BUTTON_GPIO_PIN, pigpio.PUD_UP)                              # (2)
pi.set_glitch_filter(BUTTON_GPIO_PIN, 100000)  # 100000 microseconds = 0.1 secs  # (3)


# Button pressed handler
def pressed(gpio_pin, level, tick):                                              # (4)
    # Get current pin state for LED.
    led_state = pi.read(LED_GPIO_PIN)                                            # (5)

    if led_state == 1:                                                           # (6)
        # LED is on, so turn it off.
        pi.write(LED_GPIO_PIN, 0)  # 0 = Pin Low = Led Off
        print("Button pressed: Led is off")
    else:  # 0
        # LED is off, so turn it on.
        pi.write(LED_GPIO_PIN, 1)  # 1 = Pin High = Led On
        print("Button pressed: Led is on")


# Register button handler.
pi.callback(BUTTON_GPIO_PIN, pigpio.FALLING_EDGE, pressed)                       # (7)

print("Press button to turn LED on and off.")

signal.pause()  # Stops program from exiting.
