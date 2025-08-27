import json
import time
from display_service import DisplayService
from InitService import InitService
from os import uname

def main():
    """Main boot function that can be interrupted with Ctrl+C"""
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
            print("✅ User configuration loaded successfully")
            print("   User ID:", userCfg.get('userID', 'Not set'))
            print("   Device ID:", userCfg.get('deviceId', 'Not set'))
            print("   Splash Logo:", userCfg.get('splashLogo', 'Default'))
            print("   Initialized:", userCfg.get('is_initialized', False))
    except Exception as error:
        print("❌ No User Config found:", error)
        print("   Continue Device Setup!")

    splashLogo = userCfg.get('splashLogo') or config['display']['splashLogo']    
    # Display the splash screen
    display.displayProgressBar(displayCfg, '', splashLogo, True )
    display.clearDisplay()

    # Check if we have extended network and Bluetooth LE capabilities with Pi Pico W if not we continue with basic capabilities.
    if uname()[4] == 'Raspberry Pi Pico W with RP2040':
        print('RPi Pico W')   # True
        if(isInitialised == False):
            # Create BLE instance and BLESimplePeripheral for device setup
            import bluetooth
            import machine
            import ubinascii
            # Get unique device ID (last 4 characters of flash ID)
            flash_id = ubinascii.hexlify(machine.unique_id()).decode()
            device_uuid = flash_id[-4:].upper()
            name = f"SmartBento-{device_uuid}"
            print(f"🔧 Generated device name: {name}")
            print(f"   Flash ID: {flash_id}")
            print(f"   Device UUID: {device_uuid}")
            from ble_simple_peripheral import BLESimplePeripheral
            
            ble = bluetooth.BLE()
            sp = BLESimplePeripheral(ble, name)
            InitService(sp)
            print("🚀 BLE InitService started. Press Ctrl+C to stop.")

    else:
    #     TO DO implement splashLogo selection with internal button. No WiFi or Bluetooth LE capabilities available.
        print('RPi Pico')     # False

if __name__ == "__main__":
    try:
        print("🔧 Starting SmartBento Device Boot Process...")
        print("   Press Ctrl+C to stop execution")
        main()
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n🛑 Boot process interrupted by user (Ctrl+C)")
        print("   Shutting down gracefully...")
        
        # Clean up any resources if needed
        try:
            # Stop BLE if it was started
            import bluetooth
            ble = bluetooth.BLE()
            if ble.active():
                print("   Stopping BLE...")
                ble.active(False)
        except:
            pass
            
        print("   Boot process stopped successfully")
        print("   Run 'main.py' to start the main application")
        
    except Exception as e:
        print(f"\n❌ Unexpected error during boot: {e}")
        print("   Boot process failed")


