# modulars project configuration

# class to define a room with a sensorID and measurement type and temp / humidity
class Sensor: 
    def __init__(self,sensorID, location, measurement):
        self.sensorID = sensorID
        self.temperature_C = 0
        self.temerature_F = 0
        self.temp_F_at_7am = 0
        self.humidity = 0
        self.location = location
        self.measurement = measurement

    def __str__(self):
        return (f'Location: {self.location}, sensorID: {self.sensorID}.')


locations = [
        Sensor(10223, 'outside', 'milan2'),
        Sensor(1687, 'room1', 'milan2'),
        Sensor(7938, 'room2', 'milan2'),
        Sensor(7024, 'room3', 'milan2'),
        Sensor(12896, 'room4', 'milan2')
    ]
    