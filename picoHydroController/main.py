import time
from periphials import Pump, Lights
from utils import load_env, publish_mqtt_message

mqtt_config = load_env()

MQTT_SERVER = mqtt_config.get('MQTT_SERVER')
MQTT_USER = mqtt_config.get('MQTT_USER')
MQTT_PASSWORD = mqtt_config.get('MQTT_PASSWORD')
MQTT_CLIENT_ID = 'SOUTH_RACK_BARLEY'

supplyPump = Pump(1)
saltPump = Pump(2)
light = Lights(3)


def controlSupplyPump():
   current_time = supplyPump.get_current_time()
   if not supplyPump.on and supplyPump.get_alarm() == 0:
      supplyPump.device_on()
      supplyPump.set_runtime_duration(5000)  # Run for 5 seconds
      print("Supply Pump ON")
   


def main():
   pass