#!/usr/bin/env python3
"""
Test script to verify device name generation
"""
import machine
import ubinascii

print("🧪 Testing device name generation...")

# Get unique device ID (last 4 characters of flash ID)
flash_id = ubinascii.hexlify(machine.unique_id()).decode()
device_uuid = flash_id[-4:].upper()
name = f"SmartBento{device_uuid}"

print(f"🔧 Generated device name: {name}")
print(f"   Flash ID: {flash_id}")
print(f"   Device UUID: {device_uuid}")
print(f"   Full name: {name}")

# Test the advertising payload generation
try:
    from ble_advertising import advertising_payload
    import bluetooth
    
    _UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
    payload = advertising_payload(name=name, services=[_UART_UUID])
    
    print(f"📡 Advertising payload generated successfully")
    print(f"   Payload length: {len(payload)} bytes")
    print(f"   Payload: {payload}")
    
except Exception as e:
    print(f"❌ Error generating advertising payload: {e}")

print("✅ Test complete!")
