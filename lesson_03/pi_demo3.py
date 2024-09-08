import asyncio
from bleak import BleakClient, BleakScanner, uuids

# Service UUID (0x1848) - normalized to 128-bit UUID
SERVICE_UUID = uuids.normalize_uuid_16(0x1848)
WRITE_CHARACTERISTIC_UUID = uuids.normalize_uuid_16(0x2A6E)  # Central writes here
READ_CHARACTERISTIC_UUID = uuids.normalize_uuid_16(0x2A6F)   # Central reads here

# List of known peripheral MAC addresses
peripheral_addresses = ["D8:3A:DD:3E:1B:6C", "D8:3A:DD:8D:CF:DE"]  # Replace with actual MAC addresses

async def send_data_task(client, peripheral_name):
    """Send data to the peripheral."""
    message = f"Hello from Central to {peripheral_name}!".encode("utf-8")
    while True:
        await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, message)
        await asyncio.sleep(2)  # Send data every 2 seconds

async def receive_data_task(client, peripheral_name):
    """Receive data from the peripheral."""
    while True:
        try:
            response = await client.read_gatt_char(READ_CHARACTERISTIC_UUID)
            print(f"Central received from {peripheral_name}: {response.decode('utf-8')}")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error receiving data from {peripheral_name}: {e}")
            break

async def handle_peripheral(address):
    """Connect to a peripheral and manage data exchange."""
    print(f"Connecting to {address}...")
    
    try:
        async with BleakClient(address) as client:
            peripheral_name = address
            print(f"Connected to {peripheral_name}")

            # Create tasks for sending and receiving data for this peripheral
            tasks = [
                asyncio.create_task(send_data_task(client, peripheral_name)),
                asyncio.create_task(receive_data_task(client, peripheral_name)),
            ]
            await asyncio.gather(*tasks)

    except Exception as e:
        print(f"Error connecting to {address}: {e}")

async def main():
    """Main function to manage connections to multiple peripherals sequentially."""
    
    for address in peripheral_addresses:
        # Connect to each peripheral sequentially
        await handle_peripheral(address)

# Run the main function to handle multiple peripherals
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
