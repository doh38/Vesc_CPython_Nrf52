import busio
import board
import terminalio
import adafruit_BLE
import asyncio
import busio
import gc

#BLE LAYOUT
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

#BLE_UART function
ble = BLERadio()
uart_BLE = UARTService()
advertisement = ProvideServicesAdvertisement(uart_BLE)
BLERadio.name = "VESC_CPython_Nrf52"

#UART VESC LAYOUT
uart_VESC = busio.UART(
            board.TX,
            board.RX,
            baudrate = 115200, # VESC UART baudrate
            timeout = 0.005, # 5ms is enough for reading the UART
            receiver_buffer_size = 1024) # VESC PACKET_MAX_PL_LEN = 512

#waker
VESC_write_array_ON= bytearray(6) #02 01 00 00 00 03
VESC_write_array_ON[0] = 0X02
VESC_write_array_ON[1] = 0X01
VESC_write_array_ON[2] = 0X00
VESC_write_array_ON[3] = 0X00
VESC_write_array_ON[4] = 0X00
VESC_write_array_ON[5] = 0X03

gc.enable()




async def BLE_handling():
    #await asyncio.sleep(0.2)
    while True:
        while not ble.connected:
            ble.stop_advertising()
            ble.start_advertising(advertisement)
            print("Waiting to connect")
            await asyncio.sleep(6)
            #print("Connected")
            
        while ble.connected:
            #print("BLE_LOOP_START")
            gc.collect()
            await asyncio.sleep(0.02)
            BTB = uart_BLE.read(3)
            await asyncio.sleep(0.05)
            if BTB:
                #print(BTB)
                try:
                    if BTB[0] == 0X02:
                        payload_len = BTB[1]
                        RBB  = uart_BLE.read(payload_len + 2)
                        await asyncio.sleep(0.02)
                        uart_VESC.write(BTB)
                        uart_VESC.write(RBB)
                        #print("BLE_02",BTB,RBB)
                        BTB = []
                        del RBB
                        await asyncio.sleep(0.02)

                    if BTB[0] == 0X03:
                        payload_len = (BTB[1] * 256) + BTB[2]
                        RBB  = uart_BLE.read(payload_len + 2 + 2)
                        await asyncio.sleep(0.02)
                        uart_VESC.write(BTB)
                        uart_VESC.write(RBB)
                        #print("BLE03",BTB,RBB)
                        BTB = []
                        del RBB
                        await asyncio.sleep(0.02)

                    else:
                        #print("bad")
                        pass
                except IndexError:
                    #print("the pass")
                    pass




async def UART_handling():
    await asyncio.sleep(0.2)
    while True:
        #await asyncio.sleep(0.04)
        TB = uart_VESC.read(3)
        await asyncio.sleep(0.02)
        #print(TB)
        if TB is not 0:
            try:
                if TB[0]  == 0X02:
                    payload_len = TB[1]
                    RVB = uart_VESC.read(  payload_len + 2)
                    await asyncio.sleep(0.02)
                    uart_BLE.write(TB)
                    #await asyncio.sleep(0.05)
                    uart_BLE.write(RVB)
                    #print("VESC_02",TB, RVB)
                    TB = []
                    del RVB
                    await asyncio.sleep(0.02)


                if TB[0] == 0X03:
                    payload_len = (TB[1] * 256) + TB[2]
                    RVB = uart_VESC.read(payload_len + 2 + 2)
                    await asyncio.sleep(0.02)
                    uart_BLE.write(TB)
                    #await asyncio.sleep(0.005)
                    uart_BLE.write(RVB)
                    #print("VESC_03",TB, RVB)
                    TB = []
                    del RVB
                    await asyncio.sleep(0.02)


            except IndexError:
                pass


async def VESC_ping():
    global VESC_write_array_ON
    while True:
        uart_VESC.write(VESC_write_array_ON)
        await asyncio.sleep(0.2)
        #print(VESC_write_array_ON)

async def main():

    #print("starting")
    #time.sleep(2) # boot init delay time so the display will be ready
    #BLE_adv_task = asyncio.create_task(BLE_adv())
    BLE_handling_task = asyncio.create_task(BLE_handling())
    UART_handling_task = asyncio.create_task(UART_handling())
    VESC_ping_task = asyncio.create_task(VESC_ping())



    await asyncio.gather(BLE_handling_task, UART_handling_task, VESC_ping_task )

asyncio.run(main())


