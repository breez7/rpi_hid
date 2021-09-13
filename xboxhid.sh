#!/bin/bash
# This must run as root!
# This creates a generic gamepad with 2 sticks, 1 dpad, and 14 buttons.

# Create nsgamepad gadget
cd /sys/kernel/config/usb_gadget/
mkdir -p nsgamepad
cd nsgamepad

# Define USB specification
echo 0x0f0d > idVendor # Linux Foundation
echo 0x00c1 > idProduct # Gamepad
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
echo 0x58 > bDeviceClass
echo 0x42 > bDeviceSubClass
echo 0x00 > bDeviceProtocol

# Perform localization
mkdir -p strings/0x409

echo "Raspberry Pi" > strings/0x409/manufacturer
echo "NSGamepad" > strings/0x409/product

# Create configuration file
mkdir -p configs/c.1/strings/0x409

echo 0x80 > configs/c.1/bmAttributes
echo 500 > configs/c.1/MaxPower # 500 mA

# xbox gamepad
mkdir -p functions/hid.usb0
echo 0 > functions/hid.usb0/protocol
echo 0 > functions/hid.usb0/subclass
echo 26 > functions/hid.usb0/report_length
echo "05010905A1010501093AA102750895018101750895010501093B810105010901A100750115002501350045019504050109900991099309928102C075011500250135004501950405091907290A81027501950881017508150026FF00350046FF00950605091901290681027508150026FF00350046FF0095020501093209358102751016008026FF7F36008046FF7F05010901A10095020501093009318102C005010901A10095020501093309348102C0C00501093AA102750895019101750895010501093B91017508950191017508150026FF00350046FF0095010600FF090191027508950191017508150026FF00350046FF0095010600FF09029102C0C0" | xxd -r -ps >  functions/hid.usb0/report_desc


ln -s functions/hid.usb0 configs/c.1/

# Activate device
ls /sys/class/udc > UDC
