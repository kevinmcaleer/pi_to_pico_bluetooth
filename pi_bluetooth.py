import bluetooth

# Search for available Bluetooth devices
print("Searching for devices...")
nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_oui=False)

if not nearby_devices:
    print("No devices found")
    exit()

for idx, (addr, name) in enumerate(nearby_devices):
    print(f"Device {idx}: {name} - {addr}")

# Assuming you know the Pico W's MAC address or selecting one found
target_address = "XX:XX:XX:XX:XX:XX"  # replace with the Pico W's Bluetooth MAC

# Create a Bluetooth socket and connect to the Raspberry Pi Pico W
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

try:
    # Connect to the target device on the same port as MicroPython Pico W
    port = 1  # default for RFCOMM
    print(f"Connecting to {target_address}...")
    sock.connect((target_address, port))
    print("Connected successfully")

    # Send data
    message = "Hello from Raspberry Pi!"
    print(f"Sending message: {message}")
    sock.send(message)

    # Receiving data from the Pico W
    data = sock.recv(1024)
    print(f"Received: {data}")

except bluetooth.btcommon.BluetoothError as err:
    print(f"Bluetooth Error: {err}")

finally:
    # Close the socket when done
    sock.close()
