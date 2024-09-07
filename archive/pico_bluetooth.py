from machine import Pin
import bluetooth

# Initialize Bluetooth on the Pico W
bt = bluetooth.BLE()
bt.active(True)

# Callback to handle BLE events
def bt_irq(event, data):
    if event == bluetooth.IRQ_CENTRAL_CONNECT:
        print("Central device connected")
    elif event == bluetooth.IRQ_CENTRAL_DISCONNECT:
        print("Central device disconnected")
    elif event == bluetooth.IRQ_GATTS_WRITE:
        conn_handle, attr_handle = data
        message = bt.gatts_read(attr_handle)
        print("Message received:", message.decode())
        # Send a response back to the Raspberry Pi
        bt.gatts_notify(conn_handle, attr_handle, b"Message received")

# Setup the BLE service and characteristic
SERVICE_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef0")
CHARACTERISTIC_UUID = bluetooth.UUID("12345678-1234-5678-1234-56789abcdef1")
CHARACTERISTIC = (CHARACTERISTIC_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_WRITE,)
SERVICE = (SERVICE_UUID, (CHARACTERISTIC,),)

# Register the service
bt.irq(bt_irq)
bt.gatts_register_services([SERVICE])

# Advertising the BLE service
def advertise(bt):
    adv_data = bluetooth.advertising_payload(name="PicoW", services=[SERVICE_UUID])
    bt.gap_advertise(100, adv_data)  # 100 ms advertising interval

advertise(bt)
print("Pico W is advertising...")
