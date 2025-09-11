from machine import Pin, I2C
import time
from abc import ABC, abstractmethod


class DeviceController(ABC):
    def __init__(self, pin_number: int):
        self.pin = Pin(pin_number, Pin.OUT)  # Set pin as output
        self.on = False  # Device state
        self.next_alarm = 0  # Next alarm time
        self.runtime = 0  # Runtime duration

    def get_current_time(self) -> int:
        return time.ticks_ms()


    def set_alarm(self, offset_ms):
        """Set the alarm for the next time the device should change state."""
        self.next_alarm = time.ticks_add(self.get_current_time(), offset_ms)

    def set_runtime_duration(self, offset_ms: int):
        """Set the runtime duration for the device."""
        self.runtime = time.ticks_add(self.get_current_time(), offset_ms)

    def get_alarm(self) -> int:
        return self.next_alarm

    def get_runtime(self) -> int:
        return self.runtime

    def device_on(self):
        self.pin.on()
        self.on = True

    def device_off(self):
        self.pin.off()
        self.on = False

class IsquaredCsensor(ABC):
    def __init__(self, serial_clock_pin: int, serial_data_pin: int, frequency: int, address: int):
        self.scl = serial_clock_pin
        self.sda = serial_data_pin
        self.freq = frequency
        self.address = address
        self.i2c = I2C(0, scl=Pin(self.scl), sda=Pin(self.sda), freq=self.freq)
    

    @abstractmethod
    def read_value(self):
        pass


class Pump(DeviceController):
    def __init__(self, pin_number):
        super().__init__(pin_number)

class Lights(DeviceController):
    def __init__(self, pin_number):
        super().__init__(pin_number)
