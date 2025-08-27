import time
import bluetooth
import machine
import json
import ubinascii
from base64 import b64decode

from ble_simple_peripheral import BLESimplePeripheral

class InitService():
    def __init__ (self, isInitialised):
        print('Initialisation started')
        self.bluetooth = bluetooth.BLE()
        self.isInitialised = isInitialised
        self.debounce_time = 0
        # Create an instance of the BLESimplePeripheral class with the BLE object
        self.blePeripheal = BLESimplePeripheral(self.bluetooth)
        
        self.initState = {'uuidSent':False,'isRegisteredToUser':False, 'wirelessOk':False}
        try:
            while True:
                if (time.ticks_ms() - self.debounce_time) > 300:
                    if self.blePeripheal.is_connected():  # Check if a BLE connection is established
                        self.blePeripheal.on_write(self.on_rx)  # Set the callback function for data reception
                        if self.initState['uuidSent']==False:
                           print(self.initState['uuidSent'])
                           self.sendUUID()
                        # Update the debounce time    
                        self.debounce_time=time.ticks_ms()
        except KeyboardInterrupt:
            pass
        
    # Define a callback function to handle received data
    def on_rx(self, data):
        print("Data received: ", data)  # Print the received data
        config = json.loads(data.decode())
        print(config);
        if config.get('connectionSuccess')==True and not config.get('userId'):
            self.initState['uuidSent']= True

        
    def sendUUID(self ):
        if self.blePeripheal.is_connected():
            UUID = ubinascii.hexlify(machine.unique_id()).decode()
            msg={}
            msg['deviceId']= UUID
            str = json.dumps(msg)
            print('Sending device Id to Phone', str)
            self.blePeripheal.send(str)
            return
        print('Sending canceled device disconected')
        