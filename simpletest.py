from time import sleep
from water_pump import WaterPump
from moisture_sensor import MoistureSensor
import os

# Scriptul ruleaza la bootare
# sudo nano /etc/profile este profilul de bash modificat
# Pentru un loop infinit
# In loc de sudo python3 /home/pi/Documents/Licenta/simpletest.py
# Scriem sudo python3 /home/pi/Documents/Licenta/simpletest.py &
# Pentru a rula in background dar fara output in consola

relay_channel = os.environ.get('RELAY_CHANNEL')
water_pump = WaterPump(relay_channel, 3)
moisture_sensor = MoistureSensor()

user_id = os.environ.get('USER_ID')
sensor_id = os.environ.get('SENSOR_ID')


for _ in range(2):
    measurement = moisture_sensor.get_measurement()
    print(measurement)
    if measurement < 35:
        water_pump.start_watering()
    sleep(10)