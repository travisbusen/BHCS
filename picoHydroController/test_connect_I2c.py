import time
from machine import I2C, Pin

def convert_celsius_to_fahrenheit(c):
    return (c * 9/5) + 32


ADDR = 0x38

# Initialize I2C
i2c = I2C(1, scl=Pin(3), sda=Pin(2), freq=100000)


time.sleep_ms(110) # only needed on first boot, but harmless to run always

#send status byte request
i2c.writeto(ADDR, b'\x71')

# read 1 bytes of status
status = i2c.readfrom(ADDR, 1)

if status == b'\x18': # bit 3 and 4 are 1 calibraded 
    print("Sensor is ready")
else:
    print("Sensor not ready, status:", status)

time.sleep_ms(10)

# send measurement command
i2c.writeto(ADDR, b'\xAC\x33\x00')

time.sleep_ms(100) # wait for measurement to complete

# read the measurement data
data = i2c.readfrom(ADDR, 6)
if (data[0] >> 7) & 1 == 0: # check if bit 7 is 0, meaning data is ready
     print("Data ready, status:", data)

## Humidity is 20 bits
## all of index 1 and 2 and first 4 bits of index 3

humidity_raw = (data[1] << 12) | (data[2] << 4) | (data[3] >> 4)
# 
humidity = (humidity_raw / 2**20) * 100
print("Humidity: %.2f%%" % humidity)

# temperature is 20 bits
# last 4 bits of index 3 and all of index 4 and 5
# 0x0F is 15 which represents the last 4 in binary (00001111)
temperature_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
temperature = ((temperature_raw / 2**20) * 200) - 50
temp2 = convert_celsius_to_fahrenheit(temperature)
print(f"Temperature: {temp2:.2f} F")