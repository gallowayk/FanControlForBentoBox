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
        self.availableSplashLogo = Logos()
        self.height = config['height']
        self.display = SSD1306_I2C(self.width, self.height, self.I2C)
        self.displayFormat = writer.Writer(self.display, freesans20)
        self.setTextPos = self.displayFormat.set_textpos
        self.applyText = self.displayFormat.printstring
        self.show = self.display.show
        self.infinte_bar = progress_bar.ProgressBar(10, 40, self.width - 20, 15, self.display)
        self._connectionState = connection_state
        if self._connectionState == False:
            self.initProgressBar()
        
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
        self.clearDisplay()
    
    def initProgressBar(self, message=''):
        #To DO implement message parser
        self.display.text('connecting to', 0, 10)
        self.display.text('network...', 0, 20)
        
    def displayProgressBar(self):
        self.infinte_bar.update()
        self.display.show()
    
    @property
    def connectionState(self):
        return self._connectionState
    
    def setConnectionState(self, value):
        self._connectionState = value
        
    def main(self, sensors):
        print('Temperature:', sensors)
        voc = sensors.voc
        count = 0
        seconds = 0
        voc_level_avg = 0
        voc_level_sum = 0
        show_temp = True
        while True:
            print('connection_state from display service: '+ str(self._connectionState))
            if self._connectionState == False:
                self.displayProgressBar()
            else:
                if count <= 49:
#                 if led_state != pico_led.value:
#                     led_state = pico_led.value
#                     webInterface.setLedStatus(led_state)
                    count += 1
                    voc_level_sum += sensors.airQualityIndex
                    voc_level_avg = voc_level_sum/count
                    bigText = self.displayFormat
                    bigText.set_textpos(0,0)
                    if voc_level_avg > 1:
                        bigText.printstring("VOC: {}  T^T".format(round(voc_level_avg,1)))
                        self.show()
                    else:
                        bigText.printstring("VOC: {}  ^_^".format(round(voc_level_avg,1)))
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
                            bigText.printstring("TEMP: {}C".format(round(temp,1)))
                            self.show()
                            time.sleep(0.5)
                            seconds += 1
                        else:
                            bigText.set_textpos(0,21)
                            bigText.printstring("%RH: {}%".format(round(humidity,2)))
                            self.show()
                            time.sleep(1)
                            seconds += 1
                    else:
                        seconds = 0
                        show_temp = not show_temp
                        self.clearDisplay(0) #clear screen of any artifacts
                        self.show()
                else:
                    count = 1  #reset counter
                    voc_level_sum = voc_level_avg #reset running sum of VOC readings
                    self.clearDisplay(0) #clear screen of any artifacts
                    self.show()
                
                if voc_level_avg >= voc.threshold:
    #                 fan_relay.on() #relay pin high
                    bigText.set_textpos(0,42)
                    bigText.printstring("FAN: ON")
    #                 led.value(1)
                else:
    #                 fan_relay.off() #relay pin low
                    bigText.set_textpos(0,42) 
                    bigText.printstring("FAN: OFF")
#                 led.value(0)
#             if (time.ticks_ms() - debounce_time) > 300:
#                 if sp.is_connected():  # Check if a BLE connection is established
#                     sp.on_write(on_rx)  # Set the callback function for data reception
#                     ledStatus = "On" if led_state == 1 else "Off"
#                     # Create a message string
#                     msg="LED State:"+ledStatus+" TEMP: {}C".format(round(temp,1))+" %RH: {}%\r\n".format(round(humidity,2))
#                     # Send the message via BLE
#                     sp.send(msg)
#                     # Update the debounce time    
#                     debounce_time=time.ticks_ms()
#             print('This message will be printed every 1 seconds')