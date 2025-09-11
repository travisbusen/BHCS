import time
from periphials import Pump, Lights

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