import busio
import board
import displayio
import terminalio
import asyncio
from adafruit_display_text import label
import adafruit_displayio_sh1106
import time
from time import sleep
from adafruit_display_text.scrolling_label import ScrollingLabel
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.rect import Rect
from digitalio import DigitalInOut, Direction, Pull

now = time.monotonic()  # Time in seconds since power on

#Buttons setup:
#button power
btn1 = DigitalInOut(board.P0_10)
btn1.direction = Direction.INPUT
btn1.pull = Pull.UP
#button down (-)
btn2 = DigitalInOut(board.P0_09)
btn2.direction = Direction.INPUT
btn2.pull = Pull.UP
#button up (+)
btn3 = DigitalInOut(board.P1_00)
btn3.direction = Direction.INPUT
btn3.pull = Pull.UP

prev_state1 = btn1.value
prev_state2 = btn2.value
prev_state3 = btn3.value


displayio.release_displays()

# Use for I2C
i2c = busio.I2C(board.P1_13, board.P1_15)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)

WIDTH = 64
HEIGHT = 132  # Change to 64 if needed
BORDER = 2
ROT = 90

display = adafruit_displayio_sh1106.SH1106(display_bus, width=WIDTH, height=HEIGHT, auto_refresh=1, rotation=ROT)

#fonts pre-loading
font_file_speed = "fonts/speed85.pcf"
fontToUse = bitmap_font.load_font(font_file_speed)

#display in-function settings
DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 132


SPEED= 0

#variables definition
speed = 0

# button task
async def button():
    while True:
        global speed
        global SPEED
        
        speed = speed + 1
        if speed > 99:
             speed = 0
        SPEED= "{:02d}".format(speed)  
        # take a break sometimes!
        rest = 0.01
        await asyncio.sleep(rest)
    
#display task
   
async def display():
    while True:
        global SPEED
        probe = time-monotonic()
        splash = displayio.Group()
        text_area_middle_middle = label.Label(font = fontToUse, text=SPEED)
        text_area_middle_middle.anchor_point = (0.45, 0.75)
        text_area_middle_middle.anchored_position = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)

        text_group = displayio.Group()

        text_group.append(text_area_middle_middle)
        
        await asyncio.sleep(0.1)
        
        #separators
        splash.append(Line(0,2,62,2,0xFFFFFF))
        splash.append(Line(0,13,62,13,0xFFFFFF))

        probe1 = time.monotonic()

        
        splash.append(text_group)
        display.show(splash)
        
        print(probe - time.monotonic())
        print(probe1 - time.monotonic())
        now = time.monotonic()

async def main():
    button_task = asyncio.create_task(button())
    display_task = asyncio.create_task(display())
    await asyncio.gather(button_task, display_task)
    
asyncio.run(main()) 
