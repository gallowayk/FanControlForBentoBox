import ssd1306
import progress_bar
import framebuf
import freesans20
import writer
import time
from machine import Pin, I2C, SoftI2C, ADC
from ssd1306 import SSD1306_I2C
from SplashLogos import Logos


class DisplayService():
    def __init__(self, connection_state, config):
        print('Display conf: ', config) 
        self.I2C = I2C(config['I2Channel'],sda=Pin(config['sda_pin']), scl=Pin(config['scl_pin']), freq=config['freq'])
        self.width = config['width']
        self.config = config
        self.availableSplashLogo = Logos()
        self.height = config['height']
        self.defaultSplashLogo = config['splashLogo']
        self.display = SSD1306_I2C(self.width, self.height, self.I2C)
        self.displayFormat = writer.Writer(self.display, freesans20)
        self.setTextPos = self.displayFormat.set_textpos
        self.applyText = self.displayFormat.printstring
        self.show = self.display.show
        
        self._connectionState = connection_state
        
    def clearDisplay(self, value=0):
        self.display.invert(0)
        self.display.fill(0)
        self.show()
        return
    
    def displaySplash(self,selectedManufacturer, timeToDisplay=5, invert=1):
        splash = getattr(self.availableSplashLogo, selectedManufacturer)
        frame = framebuf.FrameBuffer(splash,self.width,self.height, framebuf.MONO_HLSB)
        self.display.invert(invert)
        self.display.fill(0)
        self.display.blit(frame,0,0)
        self.display.show()
        time.sleep(timeToDisplay)
        
    def displayProgressBar(self, config=None, message='', splashLogo = 'Bento', displayLogo = False):
        cfg = config.get('progressBar')
        timeToDisplay = cfg.get('timeToDisplay')
        if displayLogo == True:
            self.displaySplash(splashLogo, timeToDisplay/10, 1)
        else:
            #To DO implement message parser
            self.display.text('connecting to', 0, 10)
            self.display.text('network...', 0, 20)
        if not cfg:
            self.infinte_bar = progress_bar.ProgressBar(10, 40, self.width - 20, 15, self.display)
        else:
            pos_x = cfg.get('pos_x')
            pos_y = cfg.get('pos_y')
            height = cfg.get('height')
            width = cfg.get('width')
            self.infinte_bar = progress_bar.ProgressBar(pos_x, pos_y, width, height, self.display)
        secondsPass = 0
        if cfg.get('timeToDisplay'):
            while secondsPass < timeToDisplay:
                start_time = time.time()
                self.infinte_bar.update()
                self.display.show()
                secondsPass += time.time() - start_time
        else:
            self.infinte_bar.update()    
            self.display.show() 
        
            
    @property
    def connectionState(self):
        return self._connectionState
    @property
    def fanState(self):
        return self._fanState
    def setConnectionState(self, value):
        self._connectionState = value
        
    def main(self, sensors):
        voc = sensors.voc
        seconds = 0
        show_temp = True
        clearDisplay = True
        while True:
            print('connection_state from display service: '+ str(self._connectionState))
            if self._connectionState == False:
                self.displayProgressBar(self.config)
            else:
                if clearDisplay == True:
                    self.clearDisplay()
                    clearDisplay = False
#                 if led_state != pico_led.value:
#                     led_state = pico_led.value
#                     webInterface.setLedStatus(led_state)
                bigText = self.displayFormat
                bigText.set_textpos(0,0)
                if sensors.airQualityIndex > 1:
                    bigText.printstring("VOC: {}  T^T".format(round(sensors.airQualityIndex,1)))
                    self.show()
                else:
                    bigText.printstring("VOC: {}  ^_^".format(round(sensors.airQualityIndex,1)))
                    self.show()
#     ###################### TEMPERATURE ########################
                temp = sensors.temperature
                humidity = sensors.humidity
#                 webInterface.setTemperature(temp)
#                 #adc_voltage = temp.read_u16() * 3.3 / 65535
#                 #cpu_temp = 27 - (adc_voltage - 0.706)/0.001721
                if seconds <= 5:
                    if show_temp:
                        bigText.set_textpos(0,21)
                        bigText.printstring("TEMP: {}C  ".format(round(temp,1)))
                        self.show()
                        time.sleep(0.5)
                        seconds += 1
                    else:
                        bigText.set_textpos(0,21)
                        bigText.printstring("RH: {}%   ".format(round(humidity,2)))
                        self.show()
                        time.sleep(0.5)
                        seconds += 1
                else:
                    seconds = 0
                    show_temp = not show_temp
                    self.show()
                
                if sensors.airQualityIndex >= voc.threshold:
    #                 fan_relay.on() #relay pin high
                    bigText.set_textpos(0,42)
                    bigText.printstring("FAN: ON ")
    #                 led.value(1)
                else:
    #                 fan_relay.off() #relay pin low
                    bigText.set_textpos(0,42) 
                    bigText.printstring("FAN: OFF ")
#                 self.show()