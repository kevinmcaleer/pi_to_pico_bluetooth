import aioble
import bluetooth
import ujson  # For handling JSON messages
from machine import ADC, Pin
import asyncio

# Define UUIDs for the service and characteristics
_SERVICE_UUID = bluetooth.UUID(0x1848)
_WRITE_CHARACTERISTIC_UUID = bluetooth.UUID(0x2A6E)  # Central writes here
_READ_CHARACTERISTIC_UUID = bluetooth.UUID(0x2A6F)   # Peripheral responds here

# ADC Channel 4 reads the temperature sensor
sensor_temp = ADC(4)
conversion_factor = 3.3 / (65535)  # Conversion factor for ADC reading to voltage

# Function to read the internal temperature
def read_temperature():
    # Read raw temperature value
    raw_value = sensor_temp.read_u16()
    voltage = raw_value * conversion_factor
    
    # Convert to temperature (in Celsius)
    temperature = 27 - (voltage - 0.706) / 0.001721
    return temperature

async def send_data_task(connection, characteristic):
    """ Continuously send the temperature data upon request """
    while True:
        # Wait for central to write data
        data = await characteristic.read()
        if data:
            try:
                # Parse the received data as JSON
                message = ujson.loads(data.decode('utf-8'))
                
                # Check if the message asks for the temperature
                if message.get('payload') == 'get temp':
                    temp = read_temperature()
                    response = {"temp": round(temp, 2)}  # Format the temperature response
                    print(f"Sending temperature: {response['temp']}°C")
                    await characteristic.write(ujson.dumps(response).encode('utf-8'))
            except Exception as e:
                print(f"Error: {e}")
        
        await asyncio.sleep(0.5)

async def run_peripheral_mode():
    """ Set up the peripheral mode """

    # Set up the Bluetooth service and characteristics
    ble_service = aioble.Service(_SERVICE_UUID)

    # Characteristic for the central to write requests (e.g., get temperature)
    write_characteristic = aioble.Characteristic(
        ble_service, _WRITE_CHARACTERISTIC_UUID,
        read=True, write=True, capture=True
    )

    # Characteristic for the peripheral to send temperature data
    read_characteristic = aioble.Characteristic(
        ble_service, _READ_CHARACTERISTIC_UUID,
        read=True, write=True, capture=True
    )

    # Register the service
    aioble.register_services(ble_service)

    print("Peripheral starting to advertise...")

    while True:
        # Advertise and wait for a central to connect
        async with await aioble.advertise(5000, name="PicoW", services=[_SERVICE_UUID]) as connection:
            print("Connected to central device!")

            # Send data when the central writes a valid request
            await send_data_task(connection, write_characteristic)

            print("Disconnected from central")

asyncio.run(run_peripheral_mode())
