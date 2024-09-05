import asyncio
from bleak import BleakScanner

async def scan_ble_devices():
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()
    
    if devices:
        for idx, device in enumerate(devices):
            print(f"Device {idx}: {device.name} - {device.address}")
    else:
        print("No devices found.")

# Run the scan
loop = asyncio.get_event_loop()
loop.run_until_complete(scan_ble_devices())
