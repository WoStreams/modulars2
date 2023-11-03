import paho.mqtt.client as mqtt, json

# MQTT connection details
MQTT_BROKER_HOST = "10.4.131.115"
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
    target_id = 10223
    if data_dict['id'] == target_id:
        print()
        temperature_F = data_dict['temperature_C'] * 9/5  + 32
        humidity = data_dict['humidity']
        print(f"Temperature when id is {target_id}: {data_dict['temperature_C']}")
        print(f"Temperature when id is {target_id}: {round(temperature_F)}")
        print(f"Humidity when id is {target_id}: { humidity }")
        



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