import json
import time
from display_service import DisplayService
from InitService import InitService
from os import uname

with open("config.json") as f:
    config = json.load(f)
userCfg = {}
isInitialised = False 
connection_state = False
displayCfg = config.get('display')
display = DisplayService(connection_state, displayCfg)
try: 
    with open("userConfig.json") as f:
        userCfg = json.load(f)
        isInitialised = True
except Exception as error:
    print(error, ' -> No User Config found. Continue Device Setup!')

splashLogo = userCfg.get('splashLogo') or config['display']['splashLogo']    
# Display the splash screen
display.displayProgressBar(displayCfg, '', splashLogo, True )
display.clearDisplay()

# Check if we have extended network and Bluetooth LE capabilities with Pi Pico W if not we continue with basic capabilities.
if uname()[4] == 'Raspberry Pi Pico W with RP2040':
    print('RPi Pico W')   # True
    if(isInitialised == False):
        InitService(isInitialised)

else:
#     TO DO implement splashLogo selection with internal button. No WiFi or Bluetooth LE capabilities available.
    print('RPi Pico')     # False


