# Vesc_CPython_Nrf52

Nrf BLE dongle for the VESC based on Circuitpython.<br />
This is the simplest dongle ever for the VESC and my first repo, be gentle :)<br />

**HARDWARE:** <br />
-Seeed Xiao Nrf52840 <br />
-4 wires + whatever connector to connect it to the vesc <br />
-> Solder 5V/GND/RX/TX to your wires/connector and that part is done

**SOFTWARE:**<br />
-connect your Seeed Xiao Nrf52840 to your PC per usb <br />
-If you don't have already CPython installed follow this tutorial: <br />
    https://wiki.seeedstudio.com/XIAO-BLE_CircutPython/
-Copy all files/folders to your Seeed Xiao Nrf52840 (except the SOURCE folder!) <br />

**INSTALLATION** <br />
-unplug the Seeed Xiao Nrf52840 from usb, connect it to the vesc, start the vesc. <br />
-it will be shown as "Vesc_CPython_Nrf52" in VESC_TOOL app. <br />
-the rest is like always :) <br />

**SOURCE:** <br />
The source is free for use modifiy. If you find it cool and want me to do more, send me a beer!  <br />
there is a little schematic (there is only 4 wires...) and a picture of my trusty vesc4 connected and running with it <br />
Please beware that some libs have been modified and compiled to work here. Replacing them will more than probably break everything. <br />

**I DIDN'T TEST THE FIRMWARE UPDATE FUNCTION SO BE WARNED!!**  <br />
!!Comes without warranty, and can break things!! <br />

Copyright 2023 Hadrien Dorfman - dodjob@yahoo.fr <br />
This is a free piece of code: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This code is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
http://www.gnu.org/licenses.
