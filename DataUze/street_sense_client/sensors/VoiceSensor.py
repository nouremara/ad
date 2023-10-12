#!/usr/bin/env python3
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
from kafka import producer

GPIO.setmode(GPIO.BCM)

class VoiceSensor:
    def __init__(self):
        self.producer = producer(bootstrap_servers='localhost:9092')

    def send_data_to_kafka(self, topic, data):
        self.producer.send(topic, value=data)
        self.producer.flush()

    def setup(self):
        ADC.setup(0x48)

    def run(self):
        count = 0
        while True:
            voiceValue = ADC.read(0)
            if voiceValue:
                print ("Value:", voiceValue)
                if voiceValue < 50:
                    print ("Voice In!! ", count)
                    count += 1

                # Send the data to Kafka
                voice_data = {'value': voiceValue, 'count': count}
                self.send_data_to_kafka('voice_sensor_topic', voice_data)

                time.sleep(0.2)

if __name__ == '__main__':
    sensor = VoiceSensor()
    sensor.setup()
    sensor.run()