"""
File: chapter08/OLED_CPU_Temp.py

Control a OLED Display.

Dependencies:
  pip3 install luma.oled
"""
from PIL import Image, ImageDraw, ImageFont                                   # (1)
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306 #, ssd1309, ssd1325, ssd1331, sh1106
from time import sleep
import os


# OLED display is using I2C at address 0x3C
serial = i2c(port=1, address=0x3C)                                            # (2)

# Or for an SPI device.
#serial = spi(port=0, device=0)


# Initialise SSD1306 OLED device on I2C
# See the Luma OLED documentation for other supported OLED devices.
device = ssd1306(serial)                                                      # (3)
device.clear()
print("Screen Dimensions (WxH):", device.size)


def get_cpu_temp():                                                           # (4)
    """
    Get CPU Temp in Celsius.
    For information on the command vcgencmd see
    https://elinux.org/RPI_vcgencmd_usage
    """
    temp = os.popen("vcgencmd measure_temp").readline() # Eg 62.5'C
    data = temp.strip().upper().replace("TEMP=", "").split("'")
    data[0] = float(data[0])

    if data[1] == 'F':  # To celsius just in case it ever returns fahrenheit
        data[0] = (data[0] - 32) * 5/9
        data[1] = 'C'

    return (data[0], data[1])  # Eg (62.5, 'C')


# Temperature thresholds used to switch thermometer icons
# Max 85'C from https://www.raspberrypi.org/documentation/faqs/#pi-performance
# Low 70'C was half way between max and idle temp in author's office.
temp_low_threshold = 60   # degrees celsius                                   # (5)
temp_high_threshold = 85  # degrees celsius


# Thermometer icons
image_high = Image.open("temp_high.png")                                      # (6)
image_med  = Image.open("temp_med.png")
image_low  = Image.open("temp_low.png")


# Scale thermometer icons (WxH)
aspect_ratio = image_low.size[0] / image_low.size[1]                          # (7)
height = 50
width = int(height * aspect_ratio)
image_high = image_high.resize((width, height))
image_med  = image_med.resize((width, height))
image_low  = image_low.resize((width, height))

refresh_secs = 0.5   # Display refresh rate                                   # (8)
high_alert = False # Used for screen blinking when high temperature

try:
    while True:
        current_temp = get_cpu_temp()
        temp_image = None
        canvas = Image.new("RGB", device.size, "black")                       # (9)
        draw = ImageDraw.Draw(canvas)                                         # (10)
        draw.rectangle(((0,0), (device.size[0]-1, device.size[1]-1)), outline="white") # Border around display.

        # Screen blinks when temperature is high.
        # When we enter the block below only the "black"
        # screen is rendered.
        if high_alert:                                                        # (11)
            device.display(canvas.convert(device.mode))
            high_alert = False # So next loop iteration will render the icon and text and recheck temp.
            sleep(refresh_secs)
            continue

        if current_temp[0] < temp_low_threshold:                              # (12)
            temp_image = image_low
            high_alert = False

        elif current_temp[0] > temp_high_threshold:
            temp_image = image_high
            high_alert = True

        else:
            temp_image = image_med
            high_alert = False
            refresh_secs = 1

        # Temperature Icon
        image_x_offset = -40                                                  # (13)
        image_y_offset = +0
        image_xy = (((device.width - temp_image.size[0]) // 2) + image_x_offset, ((device.height - temp_image.size[1]) // 2) + image_y_offset)
        canvas.paste(temp_image, image_xy)                                    # (14)

        # Temperature Text (\u00b0 is a 'degree' symbol)                      # (15)
        text = "{}\u00b0{}".format(current_temp[0], current_temp[1])  # Eg 43'C

        # For a list of fonts available run the command "fc-list" in a terminal.

        font = None # Use a default font.                                     # (16)
        # font = ImageFont.truetype(font="Lato-Semibold.ttf", size=20)

        text_size = draw.textsize(text, font=font)                            # (17)
        text_x_offset = +15
        text_y_offset = 0
        text_xy = (((device.width - text_size[0]) // 2) + text_x_offset, ((device.height -  text_size[1]) // 2) + text_y_offset)
        draw.text(text_xy, text, fill="white", font=font)                     # (18)

        # Render display with canvas
        device.display(canvas.convert(device.mode))                           # (19)
        sleep(refresh_secs)

except KeyboardInterrupt:
    print("Bye")

finally:
    # Cleanup
    device.clear()


