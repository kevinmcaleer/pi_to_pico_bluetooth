import asyncio
from bleak import BleakClient

# Replace with the MAC address of your Raspberry Pi Pico W
pico_address = "D8:3A:DD:3E:1B:6C"  # Update this with your Pico W's address

# Use the full 128-bit UUIDs
SERVICE_UUID = "00001848-0000-1000-8000-00805f9b34fb"  # Service UUID (0x1848)
CHARACTERISTIC_UUID = "00002A6E-0000-1000-8000-00805f9b34fb"  # Characteristic UUID (0x2A6E)

async def connect_and_communicate(address):
    print(f"Connecting to {address}...")

    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        # Writing a message to the Pico W
        message = "Hello from Raspberry Pi!".encode("utf-8")
        print(f"Sending message: {message}")
        await client.write_gatt_char(CHARACTERISTIC_UUID, message)

        # Reading response from the Pico W
        response = await client.read_gatt_char(CHARACTERISTIC_UUID)
        print(f"Received: {response.decode('utf-8')}")

# Run the connection and communication
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_and_communicate(pico_address))
