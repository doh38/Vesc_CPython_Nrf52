# Vesc_CPython_Nrf52

Nrf BLE dongle for the VESC based on Circuitpython.
This is the simplest dongle ever for the VESC and my first repo, be gentle :)

**HARDWARE:**
-Seeed Xiao Nrf52840 
-4 wires + whatever connector to connect it to the vesc

-> Solder 5V/GND/RX/TX to your wires/connector and that part is done


**SOFTWARE:**
-connect your Seeed Xiao Nrf52840 to your PC per usb
-If you don't have already CPython installed follow this tutorial:
    https://wiki.seeedstudio.com/XIAO-BLE_CircutPython/
-Copy all files/folders to your Seeed Xiao Nrf52840 (except the SOURCE folder!)

**INSTALLATION**
-unplug the Seeed Xiao Nrf52840 from usb, connect it to the vesc, start the vesc.
-it will be shown as "Vesc_CPython_Nrf52" in VESC_TOOL app.
-the rest is like always :)

**SOURCE:**
The source is free for use modifiy. If you find it cool and want me to do more, send me a beer! 
there is a little schematic (there is only 4 wires...) and a picture of my trusty vesc4 connected and running with it
Please beware that some libs have been modified and compiled to work here. Replacing them will more than probably break everything.

**I DIDN'T TEST THE FIRMWARE UPDATE SO BE WARNED!!** 
!!Comes without warranty, and can break things!!
