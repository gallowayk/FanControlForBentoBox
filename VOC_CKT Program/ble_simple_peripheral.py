# This example demonstrates a UART periperhal.
import bluetooth
import random
import struct
import time
import machine
import ubinascii
from ble_advertising import advertising_payload

from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


# Get unique device ID (last 4 characters of flash ID)
flash_id = ubinascii.hexlify(machine.unique_id()).decode()
device_uuid = flash_id[-4:].upper()
name = f"SmartBento-{device_uuid}"
print(f"🔧 Generated device name: {name}")
print(f"   Flash ID: {flash_id}")
print(f"   Device UUID: {device_uuid}")

class BLESimplePeripheral:
    def __init__(self, ble, name=name):
        self._ble = ble
        
        # Method 2: Hard Reset with Cleanup
        print("🔄 Performing BLE hard reset with cleanup...")
        
        # Stop advertising and disconnect all connections
        try:
            self._ble.gap_advertise(None)  # Stop advertising
            print("   ✅ Advertising stopped")
        except:
            print("   ⚠️ No active advertising to stop")
        
        # Turn off BLE
        self._ble.active(False)
        print("   ✅ BLE turned off")
        
        # Clean up memory
        import gc
        gc.collect()
        print("   ✅ Memory cleanup complete")
        
        # Wait for cleanup
        import time
        time.sleep(1)
        print("   ⏳ Waited for cleanup")
        
        # Restart BLE
        self._ble.active(True)
        print("✅ BLE hard reset complete")
        
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._ble.gatts_set_buffer(self._handle_rx, 517)
        self._connections = set()
        self._write_callback = None
        
        # Generate device name: SmartBento + 4-letter UUID
        if name is None:
            # Get unique device ID (last 4 characters of flash ID)
            flash_id = ubinascii.hexlify(machine.unique_id()).decode()
            device_uuid = flash_id[-4:].upper()
            name = f"SmartBento-{device_uuid}"
            print(f"🔧 Generated device name: {name}")
            print(f"   Flash ID: {flash_id}")
            print(f"   Device UUID: {device_uuid}")
        else:
            print(f"🔧 Using provided device name: {name}")
        
        print(f"📡 Setting up BLE advertising with name: {name}")
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()

    def _irq(self, event, data):
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def send(self, data):
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    def is_connected(self):
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def on_write(self, callback):
        self._write_callback = callback


def demo():
    ble = bluetooth.BLE()
    ble.config(rxbuf=517)
    p = BLESimplePeripheral(ble)

    def on_rx(v):
        print("RX", v)

    p.on_write(on_rx)

    i = 0
    while True:
        if p.is_connected():
            # Short burst of queued notifications.
            for _ in range(3):
                data = str(i) + "_"
                print("TX", data)
                p.send(data)
                i += 1
        time.sleep_ms(100)


if __name__ == "__main__":
    demo()