import asyncio
from bleak import BleakClient

# Replace with the MAC address of your Raspberry Pi Pico W
pico_address = "D8:3A:DD:3E:1B:6C"  # Update this with your Pico W's address

# Use the full 128-bit UUIDs
SERVICE_UUID = "00001848-0000-1000-8000-00805f9b34fb"  # Service UUID
WRITE_CHARACTERISTIC_UUID = "00002A6E-0000-1000-8000-00805f9b34fb"  # Central writes here
READ_CHARACTERISTIC_UUID = "00002A6F-0000-1000-8000-00805f9b34fb"   # Central reads here

async def send_data_task(client):
    """Send data to the peripheral device."""
    message = "Hello from Central!".encode("utf-8")
    while True:
        print(f"Central sending: {message}")
        await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, message)
        await asyncio.sleep(2)

async def receive_data_task(client):
    """Receive data from the peripheral device."""
    while True:
        try:
            print("Central waiting for data from peripheral...")
            response = await client.read_gatt_char(READ_CHARACTERISTIC_UUID)
            print(f"Central received: {response.decode('utf-8')}")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error receiving data: {e}")
            break

async def connect_and_communicate(address):
    """Connect to the peripheral and manage data exchange."""
    print(f"Connecting to {address}...")

    async with BleakClient(address) as client:
        print(f"Connected: {client.is_connected}")

        # Create tasks for sending and receiving data
        tasks = [
            asyncio.create_task(send_data_task(client)),
            asyncio.create_task(receive_data_task(client)),
        ]
        await asyncio.gather(*tasks)

# Run the connection and communication
loop = asyncio.get_event_loop()
loop.run_until_complete(connect_and_communicate(pico_address))
