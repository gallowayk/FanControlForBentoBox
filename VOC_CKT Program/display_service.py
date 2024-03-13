import ssd1306
import framebuf
import freesans20
import writer
import time
from machine import Pin, I2C, SoftI2C, ADC
from ssd1306 import SSD1306_I2C
from SplashLogos import Logos

class DisplayService():
    def __init__(self, sensors={}, width=128, height=64):
        self.I2C = I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
        self.width = width
        self.availableSplashLogo = Logos()
        self.height = height
        self.display = SSD1306_I2C(self.width, self.height, self.I2C)
        self.displayFormat = writer.Writer(self.display, freesans20)
        self.setTextPos = self.displayFormat.set_textpos
        self.applyText = self.displayFormat.printstring
        self.show = self.display.show
        self.sensors = sensors
        
    def clearDisplay(self, value=0):
        self.display.invert(0)
        self.display.fill(0)
        self.show()
        return
    
    def setSensors(self, sensors):
        self.sensors = sensors
        
    def getSensors():
        return self.sensors
    
    def displaySplash(self,selectedManufacturer, timeToDisplay=5, invert=1):
        splash = getattr(self.availableSplashLogo, selectedManufacturer)
        frame = framebuf.FrameBuffer(splash,self.width,self.height, framebuf.MONO_HLSB)
        self.display.invert(invert)
        self.display.fill(0)
        self.display.blit(frame,0,0)
        self.display.show()
        time.sleep(timeToDisplay)
        self.clearDisplay()
        
    def startTransmission(self, sensors):
        return
        
        
    