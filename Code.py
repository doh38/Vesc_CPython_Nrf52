import busio
import board
import displayio
import terminalio
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


#TODO Make a splash branding tralala
color_bitmap = displayio.Bitmap(64, 132, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0xFFFFFF
display.show(splash)

#variables definition
speed = 0
battery = 0
light = "a"
LVL= 0
MODE = 1

#LOOP START
while True:
    #button
    cur_state1 = btn1.value
    if cur_state1 != prev_state1:
        if not cur_state1:
            print("BTN1 is down")
        
    cur_state2 = btn2.value
    if cur_state2 != prev_state2:
        if not cur_state2:
            if LVL <= 0:
                LVL = 3
            else:
                LVL = LVL - 1
            print("BTN2 is down")
        
    cur_state3 = btn3.value
    if cur_state3 != prev_state3:
        if not cur_state3:
            if LVL >= 3:
                LVL == 0
            else:
                LVL = LVL + 1
            print("BTN3 is down")
        

    LV1 = " 1 "
    LV2 = " 2 "
    LV3 = " 3 "

    SPEED= "{:02d}".format(speed)
    RANGE = " 056.6"
    POWER = "525"
    HPOW = "156"
    UNIT = "KM"
    LIGHT = light
    BATT_LVL = 100 #float(battery)
    B_PIX = round((BATT_LVL * 0.57))
    
    #display task
   
    if (now + 0.4) < time.monotonic():  # If 3 milliseconds elapses
        splash = displayio.Group()
        if LVL == 1:
            text_area_top_left = label.Label(terminalio.FONT, text=LV1, color = 0x0000FF, background_color = 0xFFFFFF)
        else:
            text_area_top_left = label.Label(terminalio.FONT, text=LV1)
        text_area_top_left.anchor_point = (-0.0, -0.0)
        text_area_top_left.anchored_position = (0, 0)

        if LVL == 2:
            text_area_top_middle = label.Label(terminalio.FONT, text=LV2, color = 0x0000FF, background_color = 0xFFFFFF)
        else:
            text_area_top_middle = label.Label(terminalio.FONT, text=LV2)
        text_area_top_middle.anchor_point = (0.5, 0.0)
        text_area_top_middle.anchored_position = (DISPLAY_WIDTH / 2, 0)

        if LVL == 3:
            text_area_top_right = label.Label(terminalio.FONT, text=LV3, color = 0x0000FF, background_color = 0xFFFFFF)
        else:
            text_area_top_right = label.Label(terminalio.FONT, text=LV3)
        text_area_top_right.anchor_point = (1.0, 0.0)
        text_area_top_right.anchored_position = (DISPLAY_WIDTH, 0)

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

        text_area_middle_middle = label.Label(font = fontToUse, text=SPEED)
        text_area_middle_middle.anchor_point = (0.45, 0.75)
        text_area_middle_middle.anchored_position = (DISPLAY_WIDTH / 2, DISPLAY_HEIGHT / 2)


        text_area_middle_right.anchor_point = (1.0, -1.1)
        text_area_middle_right.anchored_position = (DISPLAY_WIDTH, DISPLAY_HEIGHT / 2)

        text_area_bottom_right = label.Label(fontToUse3, text=LIGHT)
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

        #separators
        splash.append(Line(0,2,62,2,0xFFFFFF))
        splash.append(Line(0,13,62,13,0xFFFFFF))
        splash.append(Line(2,88,46,88,0xFFFFFF))
        splash.append(Line(0,2,0,13,0xFFFFFF))
        splash.append(Line(63,2,63,13,0xFFFFFF))
        #power level spearator
        #splash.append(RoundRect(0, 2, 15, 13, 1, fill=0x0, outline=0xFFFFFF, stroke=1))
        #splash.append(RoundRect(24, 2, 15, 13, 1, fill=0x0, outline=0xFFFFFF, stroke=1))
        #splash.append(RoundRect(49, 2, 15, 13, 1, fill=0x0, outline=0xFFFFFF, stroke=1))
        #battery
        splash.append(RoundRect(0, 114, 60, 16, 2, fill=0x0, outline=0xFFFFFF, stroke=2)) #main body
        splash.append(Line(62,118,62,126,0xFFFFFF)) #knob
        splash.append(Line(63,118,63,126,0xFFFFFF)) #knob
        splash.append(Rect(2, 117, B_PIX, 10, fill=0xFFFFFF)) #batery level 100-> 54
        splash.append(Line(2,116,2,127,0x0)) #separator (0%)
        splash.append(Line(13,116,13,127,0x0)) #separator (20%)
        splash.append(Line(24,116,24,127,0x0)) #separator
        splash.append(Line(35,116,35,127,0x0)) #separator
        splash.append(Line(46,116,46,127,0x0)) #separator
        splash.append(Line(57,116,57,127,0x0)) #separator
        splash.append(text_group)
        display.show(splash)
        now = time.monotonic()

    speed = speed + 1
    if speed > 99:
         speed = 0
    #print(speed)
    print(LVL)
    battery = battery + 1
    if battery > 99:
        battery = 0
    #print(battery)
    
    if speed%3 == 0:
        light="l"
    else:
        light = "a"
    #print(light)

    if speed%6 ==0:
        MODE = MODE + 1
    if MODE > 3:
        MODE = 1
    sleep(0.001)
    pass
