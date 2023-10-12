from confluent_kafka import Consumer, KafkaError
import configparser
import json

# Load configuration file
config = configparser.ConfigParser()
config.read('kafka_config.yaml')

# Set up Kafka consumer configuration from the configuration file
consumer_conf = {
    'bootstrap.servers': config['kafka']['bootstrap_servers'],
    'group.id': 'sensor-consumer-group',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(consumer_conf)
consumer.subscribe(['gas_sensor_topic', 'dht11_sensor_topic', 'lidar_sensor_topic', 'voice_sensor_topic'])

if __name__ == '__main__':
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print('Reached end of topic %s [%d]' % (msg.topic(), msg.partition()))
            else:
                print('Error while consuming message: %s' % msg.error().str())
        else:
            data = json.loads(msg.value().decode('utf-8'))
            print(f"Received data from topic {msg.topic()}: {data}")