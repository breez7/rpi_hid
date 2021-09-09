#!/bin/bash
cd /sys/kernel/config/usb_gadget/
mkdir -p piproxy
cd piproxy
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Raspberry Pi" > strings/0x409/manufacturer
echo "pizero keyboard Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 1: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower

# Add functions here

#keyboard
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 8 > functions/hid.usb0/report_length
#echo -ne "05010906a101050719e029e71500250175019508810295017508810195057501050819012905910295037501910195067508150026ff00050719002aff008100c0" > functions/hid.usb0/report_desc
echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xfb\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\xdd\\x05\\x07\\x19\\x00\\x29\\xdd\\x81\\x00\\xc0 > functions/hid.usb0/report_desc
ln -s functions/hid.usb0 configs/c.1/

# mouse
mkdir -p functions/hid.usb1
echo 2 > functions/hid.usb1/protocol
echo 1 > functions/hid.usb1/subclass
echo 3 > functions/hid.usb1/report_length
echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x01\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x02\\x81\\x06\\xc0\\xc0 > functions/hid.usb1/report_desc
ln -s functions/hid.usb1 configs/c.1/
# End functions

FILE1=/backingfiles/music_disk.bin
mkdir -p /backingfiles/music.d 
mount -o loop,ro,offset=$((2048*512)) -t vfat $FILE1 /backingfiles/music.d
mkdir -p functions/mass_storage.usb2 
echo 1 > functions/mass_storage.usb2/stall 
echo 0 > functions/mass_storage.usb2/lun.0/cdrom 
echo 0 > functions/mass_storage.usb2/lun.0/nofua 
echo $FILE1 > functions/mass_storage.usb2/lun.0/file
ln -s functions/mass_storage.usb2 configs/c.1/

FILE2=/backingfiles/cam_disk.bin
mkdir -p /backingfiles/cam.d 
mount -o loop,ro,offset=$((2048*512)) -t vfat $FILE2 /backingfiles/cam.d
mkdir -p functions/mass_storage.usb3 
echo 1 > functions/mass_storage.usb3/stall 
echo 0 > functions/mass_storage.usb3/lun.0/cdrom 
echo 0 > functions/mass_storage.usb3/lun.0/nofua 
echo $FILE2 > functions/mass_storage.usb3/lun.0/file
ln -s functions/mass_storage.usb3 configs/c.1/

ls /sys/class/udc > UDC

