#!/usr/bin/env python3
import PCF8591 as ADC
import RPi.GPIO as GPIO
import time
from confluent_kafka import serializing_producer


class GasSensor:
    def __init__(self):
        self.producer = producer(bootstrap_servers='localhost:9092')
        ADC.setup(0x48)
        GPIO.setup(DO, GPIO.IN)
        GPIO.setup(Buzz, GPIO.OUT)
        GPIO.output(Buzz, 1)

    def send_data_to_kafka(self, topic, data):
        self.producer.send(topic, value=data)
        self.producer.flush()

    def read_gas_level(self):
        status = 1
        count = 0
        while True:
            sensorValue = ADC.read(AIN)
            tmp = GPIO.input(DO)
            print('sensor value : ', sensorValue)
            print('sensor signal: ', tmp)

            if tmp == status:
                self.print_status(tmp)
                status = tmp
            if status == 0:
                count += 1
                if count % 2 == 0:
                    GPIO.output(Buzz, 1)
                else:
                    GPIO.output(Buzz, 0)
            else:
                GPIO.output(Buzz, 1)
                count = 0

            # Send the data to Kafka
            self.send_data_to_kafka('gas_sensor_topic', {'value': sensorValue, 'signal': tmp})

            time.sleep(0.2)

    def print_status(self, x):
        if x == 1:
            print('')
            print('   *********')
            print('   * Safe~ *')
            print('   *********')
            print('')
        if x == 0:
            print('')
            print('   ***************')
            print('   * Danger Gas! *')
            print('   ***************')
            print('')

    def destroy(self):
        GPIO.output(Buzz, 1)
        GPIO.cleanup()


if __name__ == '__main__':
    sensor = GasSensor()
    try:
        sensor.read_gas_level()
    except KeyboardInterrupt:
        sensor.destroy()
