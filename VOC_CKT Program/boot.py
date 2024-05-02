import json
from display_service import DisplayService
from os import uname

with open("config.json") as f:
    config = json.load(f)
    
connection_state = False
display = DisplayService(connection_state, config['display'])

# Check if we have extended network and Bluetooth LE capabilities with Pi Pico W if not we continue with basic capabilities.
if uname()[4] == 'Raspberry Pi Pico W with RP2040':
    print('RPi Pico W')   # True    
    display.displaySplash('Creality')
    display.clearDisplay()
else:
    print('RPi Pico')     # False
    display.displaySplash('Creality')
    display.clearDisplay()