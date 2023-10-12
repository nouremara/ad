from confluent_kafka import Producer
import time
import json
import configparser
from Sensors import GasSensor, Dht11Sensor, LidarSensor, VoiceSensor
# Load configuration file
config = configparser.ConfigParser()
config.read('path_to_your_config_file.ini')  # Replace with the path to your configuration file

# Extract Kafka producer configuration from the configuration file
kafka_conf = {
    'bootstrap.servers': config['kafka']['bootstrap_servers'],
    'client.id': 'sensor-producer'
}

producer = Producer(kafka_conf)

def send_to_kafka(topic, data):
    producer.produce(topic, key=str(time.time()), value=json.dumps(data))
    producer.flush()

# Import sensors


if __name__ == '__main__':
    gas_sensor = GasSensor()
    dht11_sensor = Dht11Sensor()
    lidar_sensor = LidarSensor()
    voice_sensor = VoiceSensor()

    while True:
        # Read sensor data
        gas_data = gas_sensor.read_gas_level()
        humidity, temperature = dht11_sensor.read_dht11_dat()
        lidar_data = lidar_sensor.run()
        voice_data = voice_sensor.run()

        # Send data to Kafka
        send_to_kafka('gas_sensor_topic', gas_data)
        send_to_kafka('dht11_sensor_topic', {'humidity': humidity, 'temperature': temperature})
        send_to_kafka('lidar_sensor_topic', lidar_data)
        send_to_kafka('voice_sensor_topic', voice_data)

        time.sleep(1)