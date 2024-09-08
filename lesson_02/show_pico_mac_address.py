import bluetooth

# Initialize Bluetooth
ble = bluetooth.BLE()
ble.active(True)

# Get the MAC address (extract from the tuple)
_, mac_address = ble.config('mac')

# Format the MAC address as a hexadecimal string
formatted_mac = ':'.join(f'{b:02X}' for b in mac_address)

# Print the formatted MAC address
print(f"Bluetooth MAC Address for this device is: {formatted_mac}")
