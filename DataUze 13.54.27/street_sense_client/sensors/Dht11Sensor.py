#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
from kafka import producer

DHTPIN = 17

GPIO.setmode(GPIO.BCM)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5

class Dht11Sensor:
    def __init__(self):
        self.producer = producer(bootstrap_servers='localhost:9092')

    def send_data_to_kafka(self, topic, data):
        self.producer.send(topic, value=data)
        self.producer.flush()

    def read_dht11_dat(self):
        # ... [Your existing code for read_dht11_dat] ...
        return the_bytes[0], the_bytes[2]

    def main(self):
        print("Raspberry Pi wiringPi DHT11 humidity and temperature sensor\n")
        while True:
            result = self.read_dht11_dat()
            if result:
                humidity, temperature = result
                print("humidity: %s %%,  Temperature: %s C`" % (humidity, temperature))

                # Send the data to Kafka
                self.send_data_to_kafka('dht11_sensor_topic', {'humidity': humidity, 'temperature': temperature})

            time.sleep(1)

    def destroy(self):
        GPIO.cleanup()

if __name__ == '__main__':
    sensor = Dht11Sensor()
    try:
        sensor.main()
    except KeyboardInterrupt:
        sensor.destroy()