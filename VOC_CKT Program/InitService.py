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
        try:
            config = json.loads(data.decode())
            print("Received config:", config);
            
            # Handle bind message with userID and deviceId
            if config.get('userID') and config.get('deviceId'):
                print("Bind message received - userID:", config.get('userID'), "deviceId:", config.get('deviceId'))
                self.createUserConfig(config.get('userID'), config.get('deviceId'))
                return
                
            # Handle legacy connectionSuccess message
            if config.get('connectionSuccess')==True and not config.get('userId'):
                self.initState['uuidSent']= True
                
        except Exception as e:
            print("Error processing received data:", e)
        
    def createUserConfig(self, userID, deviceId):
        """Create userConfig.json with userID and deviceId, then verify and send success"""
        try:
            user_config = {
                'userID': userID,
                'deviceId': deviceId,
                'splashLogo': 'SmartBento',
                'is_initialized': True,
                'registration_date': time.time()
            }
            
            # Save the configuration
            with open("userConfig.json", "w") as f:
                json.dump(user_config, f)
            
            print("User configuration saved successfully")
            
            # Read it back to verify
            try:
                with open("userConfig.json", "r") as f:
                    saved_config = json.load(f)
                
                print("✅ Configuration verified - userConfig.json contents:")
                print("   User ID:", saved_config.get('userID'))
                print("   Device ID:", saved_config.get('deviceId'))
                print("   Splash Logo:", saved_config.get('splashLogo'))
                print("   Initialized:", saved_config.get('is_initialized'))
                print("   Registration Date:", saved_config.get('registration_date'))
                
                # Send success response back to Android app
                success_response = {
                    'type': 'bind_response',
                    'status': 'success',
                    'message': 'Device bound successfully',
                    'userID': saved_config.get('userID'),
                    'deviceId': saved_config.get('deviceId')
                }
                
                self.blePeripheal.send(json.dumps(success_response))
                print("✅ Success response sent to Android app")
                
                # Update initialization state
                self.initState['isRegisteredToUser'] = True
                self.isInitialised = True
                
            except Exception as read_error:
                print("❌ Error reading back config:", read_error)
                # Send error response
                error_response = {
                    'type': 'bind_response',
                    'status': 'error',
                    'message': 'Config saved but could not verify'
                }
                self.blePeripheal.send(json.dumps(error_response))
                
        except Exception as e:
            print("❌ Error creating user config:", e)
            # Send error response
            error_response = {
                'type': 'bind_response',
                'status': 'error',
                'message': f'Failed to save config: {str(e)}'
            }
            self.blePeripheal.send(json.dumps(error_response))
        
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
        