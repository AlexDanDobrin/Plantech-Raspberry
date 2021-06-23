import RPi.GPIO as GPIO
from time import sleep

class WaterPump:

    def __init__(self, channel, duration):
        self.relay_channel = channel
        self.duration = duration
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.relay_channel, GPIO.OUT)

    def pump_on(self):
        GPIO.output(self.relay_channel, GPIO.HIGH)

    def pump_off(self):
        GPIO.output(self.relay_channel, GPIO.LOW)

    def start_watering(self):
        self.pump_on()
        sleep(self.duration)
        self.pump_off()
        GPIO.cleanup