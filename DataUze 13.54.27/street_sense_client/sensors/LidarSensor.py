import os
import ydlidar
import sys
sys.path.append("/Users/nourmac/pythonProject/YDLidar-SDK")
import time
import sys
from matplotlib.patches import Arc
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from kafka import producer

RMAX = 32.0

class LidarSensor:
    def __init__(self):
        self.producer = producer(bootstrap_servers='localhost:9092')

    def send_data_to_kafka(self, topic, data):
        self.producer.send(topic, value=data)
        self.producer.flush()

    def run(self):
        fig = plt.figure()
        lidarPolar = plt.subplot(polar=True)
        lidarPolar.autoscale_view(True, True, True)
        lidarPolar.set_rmax(RMAX)
        lidarPolar.grid(True)

        ydlidar.os_init()
        ports = ydlidar.lidarPortList()
        port = "/dev/ydlidar"
        for key, value in ports.items():
            port = value

        laser = ydlidar.CYdLidar()
        laser.setlidaropt(ydlidar.LidarPropSerialPort, port)
        laser.setlidaropt(ydlidar.LidarPropSerialBaudrate, 230400)
        laser.setlidaropt(ydlidar.LidarPropLidarType, ydlidar.TYPE_TRIANGLE)
        laser.setlidaropt(ydlidar.LidarPropDeviceType, ydlidar.YDLIDAR_TYPE_SERIAL)
        laser.setlidaropt(ydlidar.LidarPropScanFrequency, 10.0)
        laser.setlidaropt(ydlidar.LidarPropSampleRate, 9)
        laser.setlidaropt(ydlidar.LidarPropSingleChannel, False)
        laser.setlidaropt(ydlidar.LidarPropMaxAngle, 180.0)
        laser.setlidaropt(ydlidar.LidarPropMinAngle, -180.0)
        laser.setlidaropt(ydlidar.LidarPropMaxRange, 32.0)
        laser.setlidaropt(ydlidar.LidarPropMinRange, 0.01)

        scan = ydlidar.LaserScan()

        def animate(num):
            r = laser.doProcessSimple(scan)
            if r:
                print("Scan received[", scan.stamp, "]:", scan.points.size(), "ranges is [", 1.0/scan.config.scan_time, "]Hz")
                angle = []
                ran = []
                intensity = []
                for point in scan.points:
                    print("angle:", point.angle, " range: ", point.range)
                    angle.append(point.angle)
                    ran.append(point.range)
                    intensity.append(point.intensity)
                lidarPolar.clear()
                lidarPolar.scatter(angle, ran, c=intensity, cmap='hsv', alpha=0.95)

                # Send the data to Kafka
                lidar_data = {'angles': angle, 'ranges': ran, 'intensities': intensity}
                self.send_data_to_kafka('lidar_sensor_topic', lidar_data)

        ret = laser.initialize()
        if ret:
            ret = laser.turnOn()
            if ret:
                ani = animation.FuncAnimation(fig, animate, interval=50)
                plt.show()
            laser.turnOff()
        laser.disconnecting()
        plt.close()

if __name__ == '__main__':
    sensor = LidarSensor()
    sensor.run()