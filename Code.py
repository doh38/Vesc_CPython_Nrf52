"""

libs need:
- adafruit_ble folder
"""

import os
import sys
import board
import busio
import digitalio

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_ble import __name__ as BLE_NAME
from adafruit_ble import __version__ as BLE_VERSION


ble = BLERadio()
uart_BLE = UARTService()
advertisement = ProvideServicesAdvertisement(uart_BLE)
uart_VESC = busio.UART(
            board.P0_31,
            board.P0_29,
            baudrate = 115200, # VESC UART baudrate
            timeout = 0.005, # 5ms is enough for reading the UART
            receiver_buffer_size = 512) # VESC PACKET_MAX_PL_LEN = 512

led = digitalio.DigitalInOut(board.LED1)
led2 = digitalio.DigitalInOut(board.LED2_B)
led.direction = digitalio.Direction.OUTPUT
led2.direction = digitalio.Direction.OUTPUT



# === scroll up to print screen ===
print()
print()
print()
print(" ---- hello ----")

while True:
    ble.start_advertising(advertisement)
    print("Waiting to connect")
    while not ble.connected:
        pass
    print("Connected")
    while ble.connected:
        rx_BLE_bytearray = uart_BLE.read(9) # add later crc and len check to adapt read length to received message
        rx_VESC_bytearray = uart_VESC.read(9)
        led.value = False
        led2.value = True
        
        if rx_BLE_bytearray:
            uart_VESC.write(rx_BLE_bytearray) # Write to VESC
            led.value = True
            led2.value = False

        if rx_VESC_bytearray:
            uart_BLE.write(rx_VESC_bytearray) #Write to BLE
            led.value = True
            led2.value = False


print("~ bye ~")
