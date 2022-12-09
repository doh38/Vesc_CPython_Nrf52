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
from adafruit_debouncer import Debouncer

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


button_1 = Debouncer(btn1, interval=0.05)
button_2 = Debouncer(btn2, interval=0.05)
button_3 = Debouncer(btn3, interval=0.05)

displayio.release_displays()
#variables definition
speed = 0
battery = 0
light = "a"
LVL= 0
MODE = 1
brightness = 1
WIDTH = 64
HEIGHT = 132  # Change to 64 if needed
BORDER = 2
ROT = 90

# Use for I2C
i2c = busio.I2C(board.P1_13, board.P1_15)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3c)

display = adafruit_displayio_sh1106.SH1106(display_bus, width=WIDTH, height=HEIGHT, auto_refresh=1, rotation=ROT, brightness = brightness)

splash = displayio.Group()
preflash = displayio.Group()
#fonts pre-loading
font_file_speed = "fonts/speed85.pcf"
fontToUse = bitmap_font.load_font(font_file_speed)
font_file_small = "fonts/display-24.pcf"
fontToUse2 = bitmap_font.load_font(font_file_small)
font_file_symbol = "fonts/display-122.pcf"
fontToUse3 = bitmap_font.load_font(font_file_symbol)

#display in-function settings
DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 132





# button task
async def inputs():
    global speed
    global battery
    global light
    global LVL
    global MODE
    global LV1
    global LV2
    global LV3
    global RANGE
    global POWER
    global HPOW
    global UNIT
    global B_PIX
    global SPEED
    global brightness

    while True:
        button_1.update()
        button_2.update()
        button_3.update()
        
        if button_1.fell: #power button
            fall = time.monotonic()
        if button_1.rose:
            rise = time.monotonic()
            if rise - fall < 0.4: # if short
                if MODE == 3:
                    MODE = 1
                else:
                    MODE = MODE + 1
            else: # if long
                print("shortpress")
        
            

        if button_2.fell: #minus button
            fall = time.monotonic()
        if button_2.rose:
            rise = time.monotonic()
            if rise - fall < 0.4: #if short
                if LVL <= 0:
                    LVL = 3
                else:
                    LVL = LVL - 1
            else: #if long
                if light == "a":
                    light = "l"
                    display.brightness = 0
                else:
                    light = "a"
                    display.brightness = 1
                    
        if button_3.fell: #plus button
            fall = time.monotonic()
        if button_3.rose:
            rise = time.monotonic()
            if rise - fall < 0.4: #if short
                if LVL >= 3:
                    LVL = 0
                else: 
                    LVL = LVL + 1
            else: #if long
                print("BTN3 longpress")

        LV1 = " 1 "
        LV2 = " 2 "
        LV3 = " 3 "

        SPEED= "{:02d}".format(speed)
        RANGE = " 056.6"
        POWER = "525"
        HPOW = "156"
        UNIT = "KM"
        BATT_LVL = 100 #float(battery)
        B_PIX = round((BATT_LVL * 0.57))

        speed = speed + 1

        #print(speed)
        #print(LVL)
        print(MODE)

        # take a break sometimes!
        rest = 0.001
        await asyncio.sleep(rest)

#display task

async def display_splash():

    while True:
        global battery
        global light
        global LVL
        global MODE
        global LV1
        global LV2
        global LV3
        global RANGE
        global POWER
        global HPOW
        global UNIT
        global B_PIX
        global SPEED
        global prev_state1
        global prev_state2
        global prev_state3
        splash = displayio.Group()
        await asyncio.sleep(0.002)

        if LVL == 1:
            text_area_top_left = label.Label(terminalio.FONT, text=LV1, color = 0x0000FF, background_color = 0xFFFFFF)
        else:
            text_area_top_left = label.Label(terminalio.FONT, text=LV1)
        text_area_top_left.anchor_point = (-0.0, -0.0)
        text_area_top_left.anchored_position = (0, 0)
        await asyncio.sleep(0.002)
        if LVL == 2:
            text_area_top_middle = label.Label(terminalio.FONT, text=LV2, color = 0x0000FF, background_color = 0xFFFFFF)
        else:
            text_area_top_middle = label.Label(terminalio.FONT, text=LV2)
        text_area_top_middle.anchor_point = (0.5, 0.0)
        text_area_top_middle.anchored_position = (DISPLAY_WIDTH / 2, 0)
        await asyncio.sleep(0.002)
        if LVL == 3:
            text_area_top_right = label.Label(terminalio.FONT, text=LV3, color = 0x0000FF, background_color = 0xFFFFFF)
        else:
            text_area_top_right = label.Label(terminalio.FONT, text=LV3)
        text_area_top_right.anchor_point = (1.0, 0.0)
        text_area_top_right.anchored_position = (DISPLAY_WIDTH, 0)

        await asyncio.sleep(0.002)

        if MODE == 1:
            text_area_middle_left = label.Label(fontToUse2, text=RANGE, scale=1)
            text_area_middle_right = label.Label(terminalio.FONT, text=UNIT)
        if MODE == 2:
            text_area_middle_left = label.Label(fontToUse2, text=POWER, scale=1)
            text_area_middle_right = label.Label(terminalio.FONT, text="MW")
        if MODE == 3:
            text_area_middle_left = label.Label(fontToUse2, text=HPOW, scale=1)
            text_area_middle_right = label.Label(terminalio.FONT, text="HW")

        text_area_middle_left.anchor_point = (0.0, -1.6)
        text_area_middle_left.anchored_position = (0, DISPLAY_HEIGHT / 2)

        text_area_middle_right.anchor_point = (1.0, -1.1)
        text_area_middle_right.anchored_position = (DISPLAY_WIDTH, DISPLAY_HEIGHT / 2)

        await asyncio.sleep(0.002)

        text_area_middle_middle = label.Label(font = fontToUse, text=SPEED)
        text_area_middle_middle.anchor_point = (0.45, 0.75)
        text_area_middle_middle.anchored_position = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)
        await asyncio.sleep(0.002)
        text_area_bottom_right = label.Label(fontToUse3, text=light)
        text_area_bottom_right.anchor_point = (1.1, 2.8)
        text_area_bottom_right.anchored_position = (DISPLAY_WIDTH, DISPLAY_HEIGHT)

        text_group = displayio.Group()
        text_group.append(text_area_top_middle)
        text_group.append(text_area_top_left)
        text_group.append(text_area_top_right)
        text_group.append(text_area_middle_middle)
        text_group.append(text_area_middle_left)
        text_group.append(text_area_middle_right)
        #text_group.append(text_area_bottom_middle)
        #text_group.append(text_area_bottom_left)
        text_group.append(text_area_bottom_right)

        await asyncio.sleep(0.002)
        probe = time.monotonic()
        #separators
        splash.append(Line(0,2,62,2,0xFFFFFF))
        await asyncio.sleep(0.002)
        splash.append(Line(0,13,62,13,0xFFFFFF))
        await asyncio.sleep(0.02)
        splash.append(Line(2,88,46,88,0xFFFFFF))
        await asyncio.sleep(0.002)
        splash.append(Line(0,2,0,13,0xFFFFFF))
        await asyncio.sleep(0.002)
        splash.append(Line(63,2,63,13,0xFFFFFF))

        await asyncio.sleep(0.002)
        #battery
        probe = time.monotonic()
        splash.append(RoundRect(0, 114, 60, 16, 2, fill=0x0, outline=0xFFFFFF, stroke=2)) #main body
        await asyncio.sleep(0.002)
        splash.append(Line(62,118,62,126,0xFFFFFF)) #knob
        await asyncio.sleep(0.002)
        splash.append(Line(63,118,63,126,0xFFFFFF)) #knob
        await asyncio.sleep(0.002)
        splash.append(Rect(2, 117, B_PIX, 10, fill=0xFFFFFF)) #batery level 100-> 54
        await asyncio.sleep(0.002)
        splash.append(Line(2,116,2,127,0x0)) #separator (0%)
        await asyncio.sleep(0.002)
        splash.append(Line(13,116,13,127,0x0)) #separator (20%)
        await asyncio.sleep(0.002)
        splash.append(Line(24,116,24,127,0x0)) #separator
        await asyncio.sleep(0.002)
        splash.append(Line(35,116,35,127,0x0)) #separator
        await asyncio.sleep(0.002)
        splash.append(Line(46,116,46,127,0x0)) #separator
        await asyncio.sleep(0.002)
        splash.append(Line(57,116,57,127,0x0)) #separator

        await asyncio.sleep(0.002)
        #print(probe - time.monotonic())
        splash.append(text_group)
        display.show(splash)

        #print(probe - time.monotonic())
        now = time.monotonic()

async def main():
    inputs_task = asyncio.create_task(inputs())
    display_splash_task = asyncio.create_task(display_splash())
    await asyncio.gather(inputs_task, display_splash_task)

asyncio.run(main())
