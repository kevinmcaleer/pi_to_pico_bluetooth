import asyncio
from bleak import BleakClient

# The MAC address of the peripheral
pico_address = "D8:3A:DD:3E:1B:6C"  # Replace with your Pico W's address
WRITE_CHARACTERISTIC_UUID = "00002A6E-0000-1000-8000-00805F9B34FB"
READ_CHARACTERISTIC_UUID = "00002A6F-0000-1000-8000-00805F9B34FB"

async def request_temperature(client):
    """Request temperature data from the Pico W"""
    request_message = {"payload": "get temp"}
    await client.write_gatt_char(WRITE_CHARACTERISTIC_UUID, ujson.dumps(request_message).encode('utf-8'))

    # Read the response (which contains the temperature)
    response = await client.read_gatt_char(READ_CHARACTERISTIC_UUID)
    print(f"Received temperature data: {response.decode('utf-8')}")

async def main():
    async with BleakClient(pico_address) as client:
        await request_temperature(client)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
