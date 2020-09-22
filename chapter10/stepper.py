"""
File: chapter10/stepper.py

Controlling a bipolar stepper motor.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from time import sleep
import pigpio

pi = pigpio.pi()

CHANNEL_1_ENABLE_GPIO = 18                                          # (1)
CHANNEL_2_ENABLE_GPIO = 16

INPUT_1A_GPIO = 23  # Blue Coil 1 Connected to 1Y                   # (2)
INPUT_2A_GPIO = 24  # Pink Coil 2  Connected to 2Y
INPUT_3A_GPIO = 20  # Yellow Coil 3 Connected to 3Y
INPUT_4A_GPIO = 21  # Orange Coil 4 Connected to 4Y

# Influences speed of motor.
# Too low a value and motor will not step
# or will step erratically.
STEP_DELAY_SECS = 0.002  # (3)

# Coil GPIOs as a list.
coil_gpios = [                                                      # (4)
    INPUT_1A_GPIO,
    INPUT_2A_GPIO,
    INPUT_3A_GPIO,
    INPUT_4A_GPIO
]

# Initialise each coil GPIO as OUTPUT.
for gpio in coil_gpios:                                             # (5)
    pi.set_mode(gpio, pigpio.OUTPUT)


def off():
    for gpio in coil_gpios:                                         # (6)
        pi.write(gpio, pigpio.HIGH)  # Coil off

off()  # All coils off

# Enable Channels (always high)
pi.set_mode(CHANNEL_1_ENABLE_GPIO, pigpio.OUTPUT)                   # (7)
pi.write(CHANNEL_1_ENABLE_GPIO, pigpio.HIGH)
pi.set_mode(CHANNEL_2_ENABLE_GPIO, pigpio.OUTPUT)
pi.write(CHANNEL_2_ENABLE_GPIO, pigpio.HIGH)


COIL_HALF_SEQUENCE = [                                              # (8)
    [0, 1, 1, 1],
    [0, 0, 1, 1],   # (a)
    [1, 0, 1, 1],
    [1, 0, 0, 1],   # (b)
    [1, 1, 0, 1],
    [1, 1, 0, 0],   # (c)
    [1, 1, 1, 0],
    [0, 1, 1, 0]    # (d)
]


COIL_FULL_SEQUENCE = [
    [0, 0, 1, 1],   # (a)
    [1, 0, 0, 1],   # (b)
    [1, 1, 0, 0],   # (c)
    [0, 1, 1, 0]    # (d)
]


sequence = COIL_HALF_SEQUENCE                                       # (9)
#sequence = COIL_FULL_SEQUENCE


# For rotate() to keep track of the sequence row it is on.
sequence_row = 0


def rotate(steps):                                                  # (10)
    """ Rotate number of steps
        use -steps to rotate in reverse """    

    global sequence_row

    direction = +1

    if steps < 0:
        direction = -1

    for step in range(abs(steps)):                                  # (11)

      coil_states = sequence[sequence_row]                          # (12)

      for i in range(len(sequence[sequence_row])):

          gpio = coil_gpios[i]                                      # (13)
          state = sequence[sequence_row][i] # 0 or 1                # (14)
          pi.write(gpio, state)                                     # (15)

          sleep(STEP_DELAY_SECS)

      sequence_row += direction                                     # (16)

      if sequence_row < 0:
          sequence_row = len(sequence) - 1
      elif sequence_row >= len(sequence):
          sequence_row = 0


if __name__ == '__main__':

    try:                                                            # (17)
        steps = 4096  # Steps for HALF stepping sequence.
        print("{} steps for full 360 degree rotation.".format(steps))
        rotate(steps)  # Rotate one direction
        rotate(-steps) # Rotate reverse direction


    finally:
        off()  # Turn stepper coils off
        pi.stop()  # PiGPIO Cleanup
