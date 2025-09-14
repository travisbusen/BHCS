from machine import Pin, I2C
import time
from abc import ABC, abstractmethod


class I2CInit:
    """
    Initialize and manage I2C communication for sensors and devices.
    
    This class handles the setup and initialization of I2C interfaces
    with configurable pins and frequencies.
    """
    def __init__(self, bus: int, serial_clock_pin: int, serial_data_pin: int, frequency: int):
        """
        Initialize I2C parameters.
        
        Args:
            bus: The I2C bus number (0 or 1 )
            serial_clock_pin: The GPIO pin number for SCL (clock)
            serial_data_pin: The GPIO pin number for SDA (data)
            frequency: The I2C bus frequency in Hz (typically 100000 or 400000)
        """
        self.bus = bus
        self.serial_clock_pin = serial_clock_pin
        self.serial_data_pin = serial_data_pin
        self.frequency = frequency

    def initiate_i2c(self):
        """
        Create and return the I2C interface with the specified parameters.
        
        Returns:
            An initialized I2C object ready for communication
        """
        self.i2c = I2C(self.bus, scl=Pin(self.serial_clock_pin), sda=Pin(self.serial_data_pin), freq=self.frequency)
        return self.i2c
    

class I2CSensor(ABC):
    """
    Abstract base class for I2C-based sensors.
    
    Provides a common interface for working with various I2C sensors,
    defining the core methods that all sensors should implement.
    """
    def __init__(self, i2c: I2C, address: int):
        """
        Initialize the I2C sensor with communication parameters.
        
        Args:
            i2c: An initialized I2C object for communication
            address: The I2C address of the sensor (typically 7-bit)
        """
        self.i2c = i2c
        self.address = address

    @abstractmethod
    def request_status(self, command: bytes) -> bool:
        """
        Request the status from the sensor.
        
        Args:
            command: The command bytes to send for status request
            
        Returns:
            True if the status is valid/ready, False otherwise
        """
        pass
        
    @abstractmethod
    def request_measurement(self, command: bytes) -> bool:
        """
        Request a new measurement from the sensor.
        
        Args:
            command: The command bytes to trigger a measurement
            
        Returns:
            True if the measurement request was successful, False otherwise
        """
        pass
        
    @abstractmethod
    def read_measurement(self, num_bytes: int) -> bytes:
        """
        Read measurement data from the sensor.
        
        Args:
            num_bytes: Number of bytes to read from the sensor
            
        Returns:
            The raw measurement data as bytes
        """
        pass


class AHT21(I2CSensor):
    """
    Implementation for the AHT21 Temperature and Humidity Sensor.
    
    This sensor communicates via I2C and provides both temperature
    and humidity readings.
    """
    def __init__(self, i2c: I2C, address: int):
        """
        Initialize the AHT21 sensor.
        
        Args:
            i2c: An initialized I2C object (already configured)
            address: The I2C address (typically 0x38)
        """
        super().__init__(i2c, address)
        time.sleep_ms(110)  # Startup delay needed for sensor initialization

    def request_status(self, command: bytes) -> bool:
        """
        Check if the sensor is calibrated and ready.
        
        Args:
            command: Status request command (typically b'\x71')
            
        Returns:
            True if the sensor is calibrated and ready
        """
        try:
            self.i2c.writeto(self.address, command)
        except Exception as e:
            return False
        status = self.i2c.readfrom(self.address, 1)
        if status == b'\x18':  # Bits 3 and 4 set indicate calibration complete
            return True
        else:
            return False

    def request_measurement(self, command: bytes) -> bool:
        """
        Request a new temperature and humidity measurement.
        
        Args:
            command: Measurement trigger command (typically b'\xAC\x33\x00')
            
        Returns:
            True if the request was successful
        """
        try:
            self.i2c.writeto(self.address, command)
        except Exception as e:
            return False
        time.sleep_ms(100)  # Measurement requires ~80ms to complete
        return True

    def read_measurement(self, num_bytes: int) -> bytes:
        """
        Read the measurement data from the sensor.
        
        Args:
            num_bytes: Number of bytes to read (typically 6-7)
            
        Returns:
            Raw measurement data bytes or empty bytes on error
        """
        try:
            data = self.i2c.readfrom(self.address, num_bytes)
            if (data[0] >> 7) & 1 == 0:  # Check if bit 7 is 0 (data ready)
                return data
            return b''  # Return empty bytes if data not ready
        except Exception as e:
            return b''
        
    def get_humidity(self, data: bytes) -> float:
        """
        Calculate relative humidity from raw sensor data.
        
        Args:
            data: Raw measurement data from read_measurement()
            
        Returns:
            Relative humidity as a percentage (0-100%)
        """
        # Extract 20-bit humidity value from bytes 1-3
        humidity_raw = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
        # Convert to relative humidity percentage
        humidity = (humidity_raw / 2**20) * 100
        return humidity
    
    def get_temperature(self, data: bytes) -> float:
        """
        Calculate temperature from raw sensor data.
        
        Args:
            data: Raw measurement data from read_measurement()
            
        Returns:
            Temperature in degrees Celsius
        """
        # Extract 20-bit temperature value from bytes 3-5
        # The lower 4 bits of byte 3 and all of bytes 4-5
        temperature_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
        # Convert to temperature in Celsius
        temperature = ((temperature_raw / 2**20) * 200) - 50
        return temperature


    


class DeviceController:
    """
    Base controller for physical devices connected to GPIO pins.
    
    Provides common functionality for time-based device control
    including alarms and runtime management.
    """
    def __init__(self, pin_number: int):
        """
        Initialize a device connected to a GPIO pin.
        
        Args:
            pin_number: The GPIO pin number the device is connected to
        """
        self.pin = Pin(pin_number, Pin.OUT)  # Set pin as output
        self.on = False  # Current device state (on/off)
        self.next_alarm = 0  # Next time to change device state
        self.runtime = 0  # Duration device should remain in current state

    def get_current_time(self) -> int:
        """
        Get the current system time in milliseconds.
        
        Returns:
            Current time in milliseconds
        """
        return time.ticks_ms()

    def set_alarm(self, offset_ms: int) -> None:
        """
        Set the alarm for the next time the device should change state.
        
        Args:
            offset_ms: Milliseconds from now to set the alarm
        """
        self.next_alarm = time.ticks_add(self.get_current_time(), offset_ms)

    def set_runtime_duration(self, offset_ms: int) -> None:
        """
        Set the runtime duration for the device.
        
        Args:
            offset_ms: Duration in milliseconds that the device should run
        """
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
