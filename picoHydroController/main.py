import utime
import requests
from  periphials import Pump, Lights
from utils import load_env, publish_mqtt_message, connect_wifi

mqtt_config = load_env()

MQTT_SERVER = mqtt_config.get('MQTT_SERVER')
MQTT_USER = mqtt_config.get('MQTT_USER')
MQTT_PASSWORD = mqtt_config.get('MQTT_PASSWORD')
MQTT_CLIENT_ID = 'SOUTH_RACK_BARLEY'
WIFI_SSID = mqtt_config.get('WIFI_SSID')
WIFI_PASSWORD = mqtt_config.get('WIFI_PASSWORD')

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
   # check if wifi is connected
   if connect_wifi(WIFI_SSID, WIFI_PASSWORD)
   pass


def mqtt_test():

   if connect_wifi(WIFI_SSID, WIFI_PASSWORD):
     
      message = {
         "device": "SOUTH_RACK_BARLEY",
         "status": "active",
         "timestamp": time.time()
      }
      publish_mqtt_message(
         client_id=MQTT_CLIENT_ID,
         broker=MQTT_SERVER.split(':')[0],
         port=int(MQTT_SERVER.split(':')[1]),
         user=MQTT_USER,
         password=MQTT_PASSWORD,
         topic="home/garden/south_rack_barley/status",
         message=message
      )




