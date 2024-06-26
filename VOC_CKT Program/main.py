import json
from machine import Pin, I2C, ADC
from picozero import pico_led
import time
import framebuf
import freesans20
import writer
import ahtx0
import _thread
from web_server import WebServer
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral
import asyncio
from os import uname
from display_service import DisplayService
from Sensors import Sensors

with open("config.json") as f:
    config = json.load(f)
    
connection_state = False
sensors = Sensors(config['sensors'])
display = DisplayService(connection_state, config['display'])

ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

# Set the debounce time to 0. Used for switch debouncing
debounce_time=0

# Create a Pin object for the onboard LED, configure it as an output

# Initialize the LED state to 0 (off)
#     led_state = 0

#GPIO Pin Number Definitions; use whatever pin numbers you want
button_pin = 7 #Pin for button
led_pin = 25 #On-board LED = GPIO25; change if using external LED
fan_pin = 22 #GPIO pin of fan relay signal

#set up button (optional)
#button = Pin(button_pin,Pin.IN, Pin.PULL_DOWN)

#LED Setup
led = Pin(led_pin, Pin.OUT)

#set up fan trigger pin
fan_relay = Pin(fan_pin, mode=Pin.OUT)

# Initialize the LED state to 0 (off)
led_state = 0
# Define a callback function to handle received data
def on_rx(data):
    print("Data received: ", data)  # Print the received data
    global led_state  # Access the global variable led_state
    if data == b'toggle\r\n':  # Check if the received data is "toggle"
        print("data is what we want", led_state, led, led.value)
        led_state = 1 - led_state  # Update the LED state
        pico_led.on() if led_state == 1 else pico_led.off() # Toggle the LED state (on/off)
        
    
async def main():
    global count, seconds, voc_level_avg, voc_level_sum, voc_def, show_temp, debounce_time, led_state, display, connection_state
    second_thread = _thread.start_new_thread(display.main, (sensors,)) 
    # Create a Bluetooth Low Energy (BLE) object
    webInterface = WebServer(sensors.temperature, pico_led, led_state, connection_state, 'iPhone 13 Pro Max', 'zakarias')
    def serveWrapper(reader, writer):
        return webInterface.serve(reader, writer, led_state)
#     task_connect = asyncio.create_task(webInterface.connect())
    asyncio.create_task(asyncio.start_server(serveWrapper, "0.0.0.0", 80))
    
    count = 0
    voc_level_sum = 0 
    # Main Loop
    while True:
        connection_state = webInterface.isConnected
        display.setConnectionState(connection_state)
        if count <= config['sensors']['voc']['avg_interval']:
            count += 1
            sensors.updateAirQualityIndex(count)
        else:
            count = 1
            
        if sensors.airQualityIndex >= sensors.voc.threshold:
            fan_relay.on() #relay pin high
            print('Fan ON')
        else: 
            print('Fan Off')
            fan_relay.off()
#         if not webInterface.isConnected:  # If not connected to Wi-Fi
#             webInterface.disconnect()       # Disconnect from current Wi-Fi network
#             webInterface.connect()    # Reconnect to Wi-Fi network
#             if led_state != pico_led.value:
#                 led_state = pico_led.value
#                 webInterface.setLedStatus(led_state)

#            webInterface.setTemperature(temp)


#            fan_relay.on() #relay pin high
#             led.value(1)
#             fan_relay.off() #relay pin low
#             led.value(0)
        if (time.ticks_ms() - debounce_time) > 300:
            if sp.is_connected():  # Check if a BLE connection is established
                sp.on_write(on_rx)  # Set the callback function for data reception
                ledStatus = "On" if led_state == 1 else "Off"
                # Create a message string
                msg="LED State:"+ledStatus+" TEMP: {}C".format(round(temp,1))+" %RH: {}%\r\n".format(round(humidity,2))
                # Send the message via BLE
                sp.send(msg)
                # Update the debounce time    
                debounce_time=time.ticks_ms()

        await asyncio.sleep(0.1)

try:
    asyncio.run(main())  # Run the main asynchronous function
finally:
    asyncio.new_event_loop() #Create a new event loopexcept Exception as e: