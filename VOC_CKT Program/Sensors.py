import ahtx0
from machine import Pin, I2C, ADC

class Sensors():
    def __init__(self, config):
        print('Sensor config: ', config)

        for key, value in config.items():
#       	This will map config dict to Sensor class properties            
            obj = type('Obj', (object,), {k: v for k, v in value.items()})()
            setattr(self, key, obj )
            
            currentSensor = getattr(self, key)
            
            if currentSensor.analog == True:
                setattr(currentSensor, 'analog_def', ADC(currentSensor.sense_pin))
            else:
                setattr(currentSensor, 'I2C', I2C(currentSensor.I2Channel, sda=Pin(currentSensor.sda_pin), scl=Pin(currentSensor.scl_pin), freq=currentSensor.freq))

        self.initAhtxSensor()
        self.initVocSensor()
        
        
    def initAhtxSensor(self):
        self.ahtx.sensor = ahtx0.AHT20(self.ahtx.I2C)
        self._temperature = self.ahtx.sensor.temperature
        self._humidity = self.ahtx.sensor.relative_humidity
    
    def initVocSensor(self):
        #           Special case for our VOC sensor used, it is for calibration.
        voc_conv = 5/65535
        setattr(self.voc, 'conversion', voc_conv)
    
    @property
    def temperature(self):
        return self.ahtx.sensor.temperature
    
    @property
    def humidity(self):
        return self.ahtx.sensor.relative_humidity
    
    @property
    def airQualityIndex(self):
        self._airQualityIndex = self.voc.analog_def.read_u16() * self.voc.conversion
        return self._airQualityIndex
        