from machine import Pin
import bluetooth
import struct

# Setup Bluetooth on Pico W
bt = bluetooth.BLE()
bt.active(True)

# Callback when a central connects to the Pico W
def bt_irq(event, data):
    if event == bluetooth.IRQ_CENTRAL_CONNECT:
        print("Connected to central device")
    elif event == bluetooth.IRQ_CENTRAL_DISCONNECT:
        print("Disconnected from central device")
    elif event == bluetooth.IRQ_GATTS_WRITE:
        conn_handle, attr_handle = data
        message = bt.gatts_read(attr_handle)
        print("Message received:", message)
        # Send back a response
        bt.gatts_notify(conn_handle, attr_handle, b"Message received")

# Register service
SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
CHARACTERISTIC_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
CHARACTERISTIC = (CHARACTERISTIC_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_WRITE,)
SERVICE = (SERVICE_UUID, (CHARACTERISTIC,),)

bt.irq(bt_irq)
bt.gatts_register_services([SERVICE])

# Set up LED to indicate connection
led = Pin(25, Pin.OUT)
led.value(0)

while True:
    # The loop keeps the program alive
    pass
