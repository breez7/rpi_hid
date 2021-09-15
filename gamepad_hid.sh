#!/bin/bash
cd /sys/kernel/config/usb_gadget/
mkdir -p piproxy
cd piproxy
echo 0x1d6b > idVendor # Linux Foundation
# echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x00c1 > idProduct # gamepad
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Raspberry Pi" > strings/0x409/manufacturer
echo "pizero keyboard Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

# xbox gamepad
mkdir -p functions/hid.usb0
echo 0 > functions/hid.usb0/protocol
echo 0 > functions/hid.usb0/subclass
# echo 8 > functions/hid.usb0/report_length
# echo "05010905a10115002501350045017501950e05091901290e81029502810105012507463b017504950165140939814265009501810126ff0046ff000930093109320935750895048102750895018101c0" | xxd -r -ps > functions/hid.usb0/report_desc
# echo 10 > functions/hid.usb0/report_length
# echo "05010905a10115002501350045017501950e05091901290e81029502810105012507463b017504950165140939814265009501810126ff0046ff00093009310932093509330934750895068102750895018101c0" | xxd -r -ps > functions/hid.usb0/report_desc
# echo 10 > functions/hid.usb0/report_length
# echo "05010905a10115002501350045017501950a05091901290a81029506810175011500250135004501950405010990099109930992810265009501810126ff0046ff00093009310932093509330934750895068102750895018101c0" | xxd -r -ps > functions/hid.usb0/report_desc
echo 10 > functions/hid.usb0/report_length
echo "05010905a10115002501350045017501950a05091901290a81029506810105012507463b01750495016514093981426500950181011581257f3581457f0930093109330934750895048102150026ff00350046ff0009320935750895028102750895018101c0" | xxd -r -ps > functions/hid.usb0/report_desc
# 16bit
# echo 14 > functions/hid.usb0/report_length
# echo "05010905a10115002501350045017501950a05091901290a81029506810175011500250135004501950405010990099109930992810265009501810116008026ff7f36008046ff7f0930093109330934751095048102150026ff00350046ff0009320935750895028102750895018101c0" | xxd -r -ps > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/

ls /sys/class/udc > UDC
