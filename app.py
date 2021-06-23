from time import sleep
from water_pump import WaterPump
from moisture_sensor import MoistureSensor
import os
import requests
from datetime import datetime

# Scriptul ruleaza la bootare
# sudo nano /etc/profile este profilul de bash modificat
# Pentru un loop infinit
# In loc de python3 /home/pi/Documents/Licenta/simpletest.py
# Scriem python3 /home/pi/Documents/Licenta/simpletest.py &
# Pentru a rula in background dar fara output in consola

relay_channel = int(os.environ.get('RELAY_CHANNEL'))
user_id = int(os.environ.get('USER_ID'))
sensor_id = int(os.environ.get('SENSOR_ID'))

water_pump = WaterPump(relay_channel, 3)
moisture_sensor = MoistureSensor()


def check_mode():
    # Verifica proprietatea auto a senzorului
    # Daca este setata pe auto atunci va efectua masuratori si irigatii automat
    # Altfel nu va masura si implicit nu va porni irigarea
    res = requests.get(f'https://127.0.0.1:5000/getWorkMode/{sensor_id}')
    body = res.json()
    if body['mode'] == 'auto':
        return True
    return False

def check_treshold():
    res = requests.get(f'https://127.0.0.1:5000/getTreshold/{sensor_id}')
    body = res.json()
    try:
        int(body['treshold'])
    except TypeError:
        return("Error")
    else:
        return int(body['treshold'])
    
def should_measure():
    res = requests.get(f'https://127.0.0.1:5000/lastMeasurement/{sensor_id}')
    data = res.json()
    last_date = data['timestamp']
    difference = datetime.now() - last_date
    if difference.total_seconds > 3600:
        return True
    return False

def register_measurement(value):
    res = requests.post(f'https://127.0.0.1:5000/newMeasurement/{sensor_id}', data={'value': value})

    
def DEMO():
    res = requests.get('https://127.0.0.1:5000/startDEMO/')

    if res.status_code == 200:
        water_pump.start_watering()
    


while True:
    # Doar pentru prezentarea licentei se verifica daca s-a actionat in manual
    # startul irigatiei pentru a demonstra conexiunea corecta
    DEMO()

    if should_measure():
        measurement = moisture_sensor.get_measurement()
        register_measurement(measurement)
        auto_mode = check_mode()
        if auto_mode:
            treshold = check_treshold()
            if isinstance(treshold, int):
                if int(measurement) < treshold:
                    water_pump.start_watering()

    # Verifica la fiecare 15 secunde daca s-a setat pe modul de lucru manual sau auto 
    sleep(15)
