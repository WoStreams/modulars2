from config import *

import paho.mqtt.client as mqtt, json

from influxdb import InfluxDBClient

from datetime import datetime, time
# example write operation and query operation to InfluxDB V1.8
username = 'python_user'
password = 'python_user_pw'
database = 'modulars_2023'
influx_host = "10.4.139.142"

query = 'select temperature from modulars;'
query_where = 'select humidity from modulars where meterID=\'12345\';'


# MQTT connection details
MQTT_BROKER_HOST = "10.4.139.142"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC = "RTL_433"

# Create an MQTT client instance
mqtt_client = mqtt.Client(client_id='mpekez')

# Callback for when the MQTT client receives a CONNACK response from the MQTT broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")

    # Subscribe to the MQTT topic
    mqtt_client.subscribe(MQTT_TOPIC)

# Callback for when a message is received on the MQTT topic
def on_message(mqtt_client, userdata, msg):
    #print("Received message " + str(msg.payload) + "' on topic '" + msg.topic + "'")
    #print(type(msg.payload))
    payload_str = msg.payload.decode('utf-8')

    # Parse the JSON string into a Python dictionary
    data_dict = json.loads(payload_str)

    # Now, data_dict contains the parsed JSON data as a dictionary
    #print(data_dict)
    #print(type(data_dict))
    #print(data_dict)

    # if sensorID in the mqtt msg = sensorID in my class list
    # update my data structure with the sensor data
    # write that data to the database

    for sensor in locations:
        if sensor.sensorID == data_dict['id']:
            print(f'Sensor found at location: {sensor.location}.')
            # You can perform further actions here if needed
            sensor.temperature_C = data_dict['temperature_C']
            sensor.temperature_F = data_dict['temperature_C'] * 9/5 + 32

            current_time = datetime.now()
            if current_time.hour == 7 and current_time.minute >= 0 and current_time.minute <=0:
                sensor.temp_F_at_7am = sensor.temperature_F
            

                data = [
                {
                    "measurement": sensor.measurement,
                    "tags": {
                        "meterID": sensor.sensorID,
                        "room_name": sensor.location
                    },
                    "fields": {
                        "temperature_F": sensor.temperature_F,
                        "temperature_C": sensor.temperature_C,
                        "temp_F_at_7am": sensor.temp_F_at_7am,
                        "humidity": sensor.humidity
                    }
                }
                ]
            else:
                data = [
                {
                    "measurement": sensor.measurement,
                    "tags": {
                        "meterID": sensor.sensorID,
                        "room_name": sensor.location
                    },
                    "fields": {
                        "temperature_F": sensor.temperature_F,
                        "temperature_C": sensor.temperature_C,
                        "humidity": sensor.humidity
                    }
                }
                ]

            client = InfluxDBClient(host = influx_host, port = 8086, username = username, password = password, database = database)

            print("Write points: {0}".format(data))
            client.write_points(data) 

    #decode message, prep record for database write

# Set the MQTT client's on_connect and on_message callbacks
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to the MQTT broker
# keepalive set to 120 secs
mqtt_client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 120)

if __name__ == "__main__":
    # Loop forever, processing MQTT messages as they come in
    mqtt_client.loop_forever()