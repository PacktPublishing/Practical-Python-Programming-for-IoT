"""
File: chapter08/passive_buzzer_rtttl.py

Making sound with PWM

Dependencies:
  pip3 install pigpio rtttl
"""
import pigpio
from time import sleep
from rtttl import parse_rtttl

pi = pigpio.pi()

# A Hardware PWM capable GPIO (12, 13, 18 or 19)
BUZZER_GPIO=12  # Hardware PWM Channel GPIO.

# Search web for "RTTTL Songs" to find other scores.
rtttl_score = parse_rtttl("Scale:d=4,o=4,b=125:8a,8b,8c#,8d,8e,8f#,8g#,8f#,8e,8d,8c#,8b,8a")      # (1)

# Use 50% for even on/off oscillation of passive buzzer.
# Note: 100% will not work becasue 100% = always on, so buzzer will never oscillate.
duty_cycle_pc = 50 # >0% to <100%

# pi.hardware_PWM() takes a duty_cycle param 0..1000000
duty_cycle = (int)(1000000 * (duty_cycle_pc / 100))

try:
    print("Playing " + rtttl_score['title'])

    for note in rtttl_score['notes']:                                                             # (2)
        frequency = int(note['frequency']) # hardware_PWM() expects an integer parameter.
        duration = note['duration'] # Milliseconds
        print(frequency, duration, duty_cycle)
        pi.hardware_PWM(BUZZER_GPIO, frequency, duty_cycle)                                       # (3)
        sleep(duration/1000)                                                                      # (4)

    print("Finished")

except KeyboardInterrupt:
    print("Bye")

finally:
    pi.hardware_PWM(BUZZER_GPIO, 0, 0) # Buzzer Off
    pi.stop() # PiGPIO Cleanup
