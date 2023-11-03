#to install influx library:
# pip3 install influxdb==5.3.1
# pip3 install influxdb-client==1.37.0

from influxdb import InfluxDBClient
# example write operation and query operation to InfluxDB V1.8
username = 'python_user'
password = 'python_user_pw'
database = 'modulars_2023'
influx_host = "10.4.131.115"

query = 'select temperature from modulars;'
query_where = 'select humidity from modulars where meterID=\'12345\';'

data = [
    {
        "measurement": "pekez",
        "tags": {
            "meterID": "12345",
            "room_name": 'StemLab'
        },
        "fields": {
            "temperature_F": 73.8,
            "temperature_C": 23.2,
            "humidity": 22
        }
    }
]

client = InfluxDBClient(host = influx_host, port = 8086, username = username, password = password, database = database)

print("Write points: {0}".format(data))
client.write_points(data)

print("Querying data: " + query)
result = client.query(query)
print("Result: {0}".format(result))
print()

print("Querying data: " + query_where)
result = client.query(query_where)
print("Result: {0}".format(result))

# Close the client connection
client.close()

