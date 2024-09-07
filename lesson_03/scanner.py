# Simple bluetooth scanner

import asyncio
from bleak import BleakScanner


async def scan_for_peripherals():
    """ Scans for bluetooth devices and prints the addresses of the ones it finds """
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Found device {device.name} with address {device.address}")

# Run the scan
loop = asyncio.get_event_loop()
loop.run_until_complete(scan_for_peripherals())