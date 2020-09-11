from datetime import datetime

import smbus2
import struct
import logging
import random

# I2C addressed of Arduinos MCU connected
from .reader import SensorValue, Reader

TEMP_1_REGISTER = 0x10  # DS18D20 ( onewire, D5 )
TEMP_2_REGISTER = 0x14  # DS18D20 ( onewire, D5 )
TEMP_3_REGISTER = 0x18  # DS18D20 ( onewire, D5 )
PRESSURE_IN_REGISTER = 0x20  # PRESSURE (analog, A1)
PRESSURE_OUT_REGISTER = 0x24  # PRESSURE (analog, A2)
PRESSURE_MIDDLE_REGISTER = 0x28  # PRESSURE (analog, A3)
FLUX_IN_REGISTER = 0x30  # FLUXMETER ( digital input, D2 )
FLUX_OUT_REGISTER = 0x34  # FLUXMETER ( digital input, D3 )
CC_CURRENT_REGISTER = 0x40  # SHUNT  ( LM358 gain 20, analog, A0  )
AC1_CURRENT_REGISTER = 0x44  # SCT013 (analog in A5)
AC2_CURRENT_REGISTER = 0x48  # SCT013 (analog in A5)
DHT11_AIR_REGISTER = 0x50  # DHT11 ( onewire, D6 )
DHT11_HUMIDITY_REGISTER = 0x54  # DHT11 ( onewire, D6 )
FLOODING_STATUS_REGISTER = 0x60  # Flooding sensor ( digital input, D7 )
WATER_LEVEL_REGISTER = 0x70  # DISTANCE ULTRASOUND SENSOR ( software serial, rxD9 txD10 )

TEMP_1_LABEL = 'temp1'  # DS18D20 ( onewire, D5 )
TEMP_2_LABEL = 'temp2'  # DS18D20 ( onewire, D5 )
TEMP_3_LABEL = 'temp3'  # DS18D20 ( onewire, D5 )
PRESSURE_IN_LABEL = 'pres1'  # PRESSURE (analog, A1)
PRESSURE_OUT_LABEL = 'pres2'  # PRESSURE (analog, A2)
PRESSURE_MIDDLE_LABEL = 'pres33'  # PRESSURE (analog, A3)
FLUX_IN_LABEL = 'flux1'  # FLUXMETER ( digital input, D2 )
FLUX_OUT_LABEL = 'flux2'  # FLUXMETER ( digital input, D3 )
CC_CURRENT_LABEL = 'cc'  # SHUNT  ( LM358 gain 20, analog, A0  )
AC1_CURRENT_LABEL = 'ac1'  # SCT013 (analog in A6)
AC2_CURRENT_LABEL = 'ac2'  # SCT013 (analog in A7)
DHT11_AIR_LABEL = 'dht_temp'  # DHT11 ( onewire, D6 )
DHT11_HUMIDITY_LABEL = 'dht_hum'  # DHT11 ( onewire, D6 )
FLOODING_STATUS_LABEL = 'flood'  # Flooding sensor ( digital input, D7 )
WATER_LEVEL_LABEL = 'water_lev'  # DISTANCE ULTRASOUND SENSOR ( software serial,

# i2c bus number depending on the hardware

DEFAULT_I2C_ADDR = 0x27
SECO_C23_I2C_BUS = 1
UDOO_NEO_I2C_BUS = 3

DEFAULT_I2C_BUS = SECO_C23_I2C_BUS

# data sizes
ARDUINO_FLOAT_SIZE = 4
ARDUINO_INT_SIZE = 2
ARDUINO_DOUBLE_SIZE = 8

DECIMALS = 1


class McuArduinoReader(Reader):

    def __init__(self, id, i2c_bus=DEFAULT_I2C_BUS, i2c_address=DEFAULT_I2C_ADDR, dummy_data=False):
        self.logger = logging.getLogger(__name__)
        self.id = id
        self.dummy_data = dummy_data
        self.bus = None
        self.i2c_bus = i2c_bus
        self.i2c_address = i2c_address

        if not self.dummy_data:
            self.bus = smbus2.SMBus()

    def read4_bytes_float(self, dev, start_reg, n_bytes=None):
        value = [0, 0, 0, 0]

        value[0] = self.bus.read_byte_data(dev, start_reg)
        value[1] = self.bus.read_byte_data(dev, start_reg + 1)
        value[2] = self.bus.read_byte_data(dev, start_reg + 2)
        value[3] = self.bus.read_byte_data(dev, start_reg + 3)

        b = struct.pack('4B', *value)
        value = struct.unpack('<f', b)

        return round(value[0], DECIMALS)

    def read2_bytes_integer(self, dev, start_reg, n_bytes=None):
        value = [0, 0]

        value[0] = self.bus.read_byte_data(dev, start_reg)
        value[1] = self.bus.read_byte_data(dev, start_reg + 1)

        b = struct.pack('BB', value[0], value[1])
        value = struct.unpack('<h', b)

        return value[0]

    def read1_byte_boolean(self, dev, start_reg):
        value = self.bus.read_byte_data(dev, start_reg)
        return value

    def generate_dummy(self):
        values = [
            TEMP_1_LABEL,
            TEMP_2_LABEL,
            PRESSURE_IN_LABEL,
            PRESSURE_OUT_LABEL,
            PRESSURE_MIDDLE_LABEL,
            FLUX_IN_LABEL,
            FLUX_OUT_LABEL,
            CC_CURRENT_LABEL,
            AC1_CURRENT_LABEL,
            AC2_CURRENT_LABEL
        ]
        data = []
        for val in values:
            data.append(
                SensorValue(self.id, val, round(random.uniform(0, 255), DECIMALS), int(datetime.now().timestamp())))
        return data

    # External MCU
    def get_temperature1(self):
        self.logger.debug("Requested temperature 1")
        value = self.read4_bytes_float(self.i2c_address, TEMP_1_REGISTER, ARDUINO_FLOAT_SIZE)
        return SensorValue(self.id, TEMP_1_LABEL, value, int(datetime.now().timestamp()))

    # External MCU
    def get_temperature2(self):
        self.logger.debug("Requested temperature 2")
        value = self.read4_bytes_float(self.i2c_address, TEMP_2_REGISTER, ARDUINO_FLOAT_SIZE)
        return SensorValue(self.id, TEMP_2_LABEL, value, int(datetime.now().timestamp()))

    # External MCU
    def get_temperature3(self):
        self.logger.debug("Requested temperature 2")
        value = self.read4_bytes_float(self.i2c_address, TEMP_3_REGISTER, ARDUINO_FLOAT_SIZE)
        return SensorValue(self.id, TEMP_3_LABEL, value, int(datetime.now().timestamp()))

    def get_pressure_in(self):
        self.logger.debug("Requested pressure in input")
        value = self.read4_bytes_float(self.i2c_address, PRESSURE_IN_REGISTER, ARDUINO_FLOAT_SIZE)
        return SensorValue(self.id, PRESSURE_IN_LABEL, value, int(datetime.now().timestamp()))

    def get_pressure_middle(self):
        self.logger.debug("Requested pressure in middle")
        value = self.read4_bytes_float(self.i2c_address, PRESSURE_MIDDLE_REGISTER, ARDUINO_FLOAT_SIZE)
        return SensorValue(self.id, PRESSURE_MIDDLE_LABEL, value, int(datetime.now().timestamp()))

    def get_pressure_out(self):
        self.logger.debug("Requested pressure in output")
        value = self.read4_bytes_float(self.i2c_address, PRESSURE_OUT_REGISTER, ARDUINO_FLOAT_SIZE)
        return SensorValue(self.id, PRESSURE_OUT_LABEL, value, int(datetime.now().timestamp()))

    def get_water_flux_in(self):
        self.logger.debug("Requested water flux in")
        value = self.read2_bytes_integer(self.i2c_address, FLUX_IN_REGISTER, ARDUINO_INT_SIZE)
        return SensorValue(self.id, FLUX_IN_LABEL, value, int(datetime.now().timestamp()))

    def get_water_flux_out(self):
        self.logger.debug("Requested water flux ouy")
        value = self.read2_bytes_integer(self.i2c_address, FLUX_OUT_REGISTER, ARDUINO_INT_SIZE)
        return SensorValue(self.id, FLUX_OUT_LABEL, value, int(datetime.now().timestamp()))

    def get_cc_current(self):
        self.logger.debug("Requested CC current from Shunt")
        value = self.read4_bytes_float(self.i2c_address, CC_CURRENT_REGISTER, ARDUINO_FLOAT_SIZE)
        return SensorValue(self.id, CC_CURRENT_LABEL, value, int(datetime.now().timestamp()))

    def get_ac_current(self, channel):
        self.logger.debug("Requested AC current from clamp ", str(channel))

        if channel == 1:
            AC_CURRENT_REGISTER = AC1_CURRENT_REGISTER
            label = AC1_CURRENT_LABEL
        elif channel == 2:
            AC_CURRENT_REGISTER = AC2_CURRENT_REGISTER
            label = AC2_CURRENT_LABEL
        else:
            raise Exception('Invalid channel')

        value = self.read4_bytes_float(self.i2c_address, AC_CURRENT_REGISTER, ARDUINO_FLOAT_SIZE)

        return SensorValue(self.id, label, value, int(datetime.now().timestamp()))

    def get_dht11_temperature(self):
        self.logger.debug("Requested internal temperature by DHT11")
        value = self.read4_bytes_float(self.i2c_address, DHT11_AIR_REGISTER, ARDUINO_FLOAT_SIZE)
        return SensorValue(self.id, DHT11_AIR_LABEL, value, int(datetime.now().timestamp()))

    def get_dht11_humidity(self):
        self.logger.debug("Requested internal temperature by DHT11")
        value = self.read4_bytes_float(self.i2c_address, DHT11_HUMIDITY_REGISTER, ARDUINO_FLOAT_SIZE)
        return SensorValue(self.id, DHT11_HUMIDITY_LABEL, value, int(datetime.now().timestamp()))

    def get_flood_status(self):
        self.logger.debug("Requested flooding status")
        value = self.read1_byte_boolean(self.i2c_address, FLOODING_STATUS_REGISTER)
        return SensorValue(self.id, FLOODING_STATUS_LABEL, value, int(datetime.now().timestamp()))

    def get_water_level(self):
        self.logger.debug("Requested tank water level")
        value = self.read2_bytes_integer(self.i2c_address, WATER_LEVEL_REGISTER, ARDUINO_INT_SIZE)
        return SensorValue(self.id, WATER_LEVEL_LABEL, value, int(datetime.now().timestamp()))

    def read(self):

        if self.dummy_data:
            return self.generate_dummy()

        self.logger.debug('Open i2c_bus %s i2c_address %s', self.i2c_bus, self.i2c_address)
        try:
            self.bus.open(self.i2c_bus)
        except Exception as e:
            raise e

        try:
            data = [
                self.get_temperature1(),
                self.get_temperature2(),
                self.get_pressure_in(),
                self.get_pressure_middle(),
                self.get_pressure_out(),
                self.get_water_flux_in(),
                self.get_water_flux_out(),
                self.get_cc_current(),
                self.get_ac_current(1),
                self.get_ac_current(2)
            ]

        except Exception as e:
            raise e

        return data

    def __str__(self):
        return 'MCU: ID: {}, I2C_ADDRESS: {}'.format(self.id, self.i2c_address)
