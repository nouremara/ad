# Streetsense Project
## Beschreibung
 Streetsense ist ein Projekt, das verschiedene Sensoren verwendet, um Daten zu sammeln und diese Daten über Kafka an 
 eine PostgreSQL-Datenbank weiterzuleiten.

 ## Voraussetzungen
 - Python 3.8 oder höher
 - Docker und Docker-Compose"
 - Kafka
 - PostgreSQL 


 ## Installation
 1. Klone das Repository:
    `git clone https://gitlab.com/uze-mobility/streetsense.git`
 2. Navigieren Sie in das Projektverzeichnis:
    `cd Streetsense`
 3. Installieren Sie die erforderlichen Python-Bibliotheken:
    `pip install -r requirements.txt`


## To-DO
- [x] Code für Sensoren schreiben
- [ ] Kafka Richtig einbinden
- [ ] Datenbank richtig aufstellen
- [ ] Testen
- [ ] backend schreiben
- [ ] Frontend


 ## Verwendung
 1. Starten Sie die Docker-Dienste:
    `docker-compose up -d`
 2. Führen Sie die Python-Skripte aus, um Daten von den Sensoren zu sammeln und an Kafka zu senden.


 ## Sensoren 
  > GasSensor
 - GasSensor: Misst das Gasniveau in der Umgebung.

  > Dht11Sensor
 - Dht11Sensor: Misst Temperatur und Luftfeuchtigkeit.

  > LidarSensor
 - LidarSensor: Misst Entfernungen mit einem Lidar.

  > VoiceSensor
 - VoiceSensor: Erkennt Geräusche oder Stimmen in der Umgebung.
 
