from machine import Pin, I2C
import time
from abc import ABC, abstractmethod



class I2CInit:
    def __init__(self, bus: int, serial_clock_pin: int, serial_data_pin: int, frequency: int):
        self.bus = bus
        self.serial_clock_pin = serial_clock_pin
        self.serial_data_pin = serial_data_pin
        self.frequency = frequency

    def initiate_i2c(self):
        self.i2c = I2C(self.bus, scl=Pin(self.serial_clock_pin), sda=Pin(self.serial_data_pin), freq=self.frequency)
        return self.i2c
    

class I2CSensor(ABC):
    def __init__(self, i2c: I2CInit, address: int):
        self.i2c = i2c
        self.address = address

    @abstractmethod
    def request_status(self, command: bytes) -> bool:
        pass
        
    @abstractmethod
    def request_measurement(self, command: bytes) -> bool:
        pass
        
    @abstractmethod
    def read_measurement(self, num_bytes: int) -> bytes:
        pass


class AHT21(I2CSensor):
    def __init__(self, i2c: I2CInit, address: int):
        super().__init__(i2c, address)
        time.sleep_ms(110) # only needed on first boot, but harmless to run always

    def request_status(self, command: bytes) -> bool:
        try:
            self.i2c.writeto(self.address, command)
        except Exception as e:
            return False
        status = self.i2c.readfrom(self.address, 1)
        if status == b'\x18': # bit 3 and 4 are 1 calibraded 
            return True
        else:
            return False

    def request_measurement(self, command: bytes) -> bool:
        try:
            self.i2c.writeto(self.address, command)
        except Exception as e:
            return False
        time.sleep_ms(100) # wait for measurement to complete
        return True

    def read_measurement(self, num_bytes: int) -> bytes:
        try:
            data = self.i2c.readfrom(self.address, num_bytes)
            if (data[0] >> 7) & 1 == 0: # check if bit 7 is 0, meaning data is ready
                return data
        except Exception as e:
            return b''
        
    def get_humidity(self, data: bytes) -> float:
        humidity_raw = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
        humidity = (humidity_raw / 2**20) * 100
        return humidity
    
    def get_temperature(self, data: bytes) -> float:
        temperature_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        temperature = ((temperature_raw / 2**20) * 200) - 50
        return temperature


    


class DeviceController:
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


class 

class IsquaredCsensor:
    def __init__(self, serial_clock_pin: int, serial_data_pin: int, frequency: int, address: int):
        self.scl = serial_clock_pin
        self.sda = serial_data_pin
        self.freq = frequency
        self.address = address
        self.i2c = I2C(0, scl=Pin(self.scl), sda=Pin(self.sda), freq=self.freq)
    

    
    def read_value(self):
        pass


class Pump(DeviceController):
    def __init__(self, pin_number):
        super().__init__(pin_number)

class Lights(DeviceController):
    def __init__(self, pin_number):
        super().__init__(pin_number)
