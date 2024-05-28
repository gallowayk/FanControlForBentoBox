import time
import bluetooth
import machine
import json
import ubinascii

from ble_simple_peripheral import BLESimplePeripheral

class InitService():
    def __init__ (self, isInitialised):
        print('Initialisation started')
        self.bluetooth = bluetooth.BLE()
        self.isInitialised = isInitialised
        self.debounce_time = 0
        # Create an instance of the BLESimplePeripheral class with the BLE object
        self.blePeripheal = BLESimplePeripheral(self.bluetooth)
        try:
            while True:
                if (time.ticks_ms() - self.debounce_time) > 300:
                    if self.blePeripheal.is_connected():  # Check if a BLE connection is established
                        self.blePeripheal.on_write(self.on_rx)  # Set the callback function for data reception
            #             ledStatus = "On" if led_state == 1 else "Off"
                        # Create a message string
                        UUID = ubinascii.hexlify(machine.unique_id()).decode()
                        msg={}
                        msg['deviceId']= UUID
                        # Send the message via BLE
                        str = json.dumps(msg)
                        print('String to send over Ble', json.dumps(msg))
                        self.blePeripheal.send(str)
                        # Update the debounce time    
                        self.debounce_time=time.ticks_ms()
        except KeyboardInterrupt:
            pass
        
    # Define a callback function to handle received data
    def on_rx(self, data):
        print("Data received: ", data)  # Print the received data
#         global led_state  # Access the global variable led_state
        if data == b'toggle\r\n':  # Check if the received data is "toggle"
            print("data is what we want", led_state, led, led.value)
#             led_state = 1 - led_state  # Update the LED state
#             pico_led.on() if led_state == 1 else pico_led.off() # Toggle the LED state (on/off)
        
    