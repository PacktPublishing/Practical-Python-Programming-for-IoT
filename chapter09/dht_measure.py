"""
File: chapter09/dht_measure.py

Measure temperature and humidity with DHT sensor.

Dependencies:
  pip3 install pigpio pigpio-dht

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
from pigpio_dht import DHT11, DHT22          # (1)

SENSOR_GPIO = 21
sensor = DHT11(SENSOR_GPIO)                  # (2)
#sensor = DHT22(SENSOR_GPIO)

if __name__ == '__main__':

    result = sensor.read(retries=2)          # (3)
    print(result)

    result = sensor.sample(samples=5)        # (4)
    print(result)

