from bluepy.btle import Scanner, Peripheral, DefaultDelegate

# Custom delegate to handle BLE notifications
class MyDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(f"Received notification from handle {cHandle}: {data}")

# Scan for devices
scanner = Scanner()
print("Scanning for BLE devices...")
devices = scanner.scan(10.0)  # Scan for 10 seconds

# List discovered devices
for idx, dev in enumerate(devices):
    print(f"Device {idx}: {dev.addr} - RSSI {dev.rssi} dB")

# Assuming you know the Pico W's MAC address, otherwise pick one from the discovered devices
target_address = "XX:XX:XX:XX:XX:XX"  # Replace with the MAC address of your Pico W

# Connect to the Pico W using its MAC address
print(f"Connecting to device {target_address}...")
try:
    peripheral = Peripheral(target_address)
    peripheral.setDelegate(MyDelegate())
    
    # Read or write characteristics
    # You can list services and characteristics here if needed:
    services = peripheral.getServices()
    for svc in services:
        print(f"Service: {svc.uuid}")
    
    # Assuming your Pico W has a specific characteristic you want to interact with:
    # You can find the characteristic using UUID, or iterate over all characteristics
    # characteristic = peripheral.getCharacteristics(uuid="12345678-1234-5678-1234-56789abcdef1")[0]
    
    # Send data
    # characteristic.write(b"Hello from Raspberry Pi!")
    
    # Listen for notifications
    while True:
        if peripheral.waitForNotifications(1.0):  # Timeout after 1 second if no notification
            print("Notification received")
except Exception as e:
    print(f"Failed to connect: {e}")
finally:
    # Disconnect when done
    peripheral.disconnect()
