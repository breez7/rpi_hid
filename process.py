
#!/usr/bin/env python2

import evdev, time
from evdev import InputDevice, categorize, ecodes

import io
from select import select
import os
import sys
from struct import pack

import threading
first = True
dev = {}

def kill():
    pid = os.getpid()
    os.kill(pid,2)
def update_usb_devices():
    global first
    while(True):
        try:
            devices = [path for path in evdev.list_devices()]
            if len(dev) == len(devices):
                time.sleep(1)

            print("#find")
            print(devices)
            dev_paths = [temp.path for temp in dev.values()]
            print(dev_paths)
            for device in devices:
                if device in dev_paths:
                    continue
                if first == False:
                    kill()
                a = InputDevice(device)
                dev[a.fd] = a
                a.grab()
                print("!!!!!!add")
            print("###find")
            dev_paths = [temp.path for temp in dev.values()]
            print(dev_paths)
            for path in dev_paths:
                if not path in devices:
                    for fd in dev.keys():
                        if dev[fd].path == path:
                            kill()
                            # dev[fd].ungrab()
                            dev[fd].close()
                            dev.pop(fd)
                            break
                            print("!!!!!!del")

            # for d in dev.values(): print(d)
            time.sleep(2)
            first = False
        except Exception as e:
            print(e)
            time.sleep(1)

t =threading.Thread(target=update_usb_devices)
t.daemon=True
t.start()
# update_usb_devices()

if not os.geteuid() == 0:
    sys.exit("\nOnly root can run this script\n")

# Load the configuration file, which is NOT an INI
config = {}
with open(os.path.dirname(os.path.abspath(__file__)) + "/config.conf") as f:
    for line in f:
        name, var = line.partition("=")[::2]
        config[name.strip()] = var.lower().strip().strip('\"')



NULL_CHAR = chr(0)
print (config["devicename"])

# while not dev:
#     try:
#         devices = [path for path in evdev.list_devices()]
#         for device in devices:
#             a = InputDevice(device)
#             dev[a.fd] = a
#             a.grab()

#         for d in dev.values(): print(d)
#     except:
#         print("No keyboard - waiting...")
#         time.sleep(1)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(bytes(report, encoding='utf8'))
def write_report_mouse(report):
    with open('/dev/hidg1', 'rb+') as fd:
        fd.write(report)

def inject_keystring(keys):
    for key in keys:
            if key == 'j':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_J)) + NULL_CHAR*5)
            elif key == 'd':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_D)) + NULL_CHAR*5)
            elif key == 'y':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_Y)) + NULL_CHAR*5)
            elif key == 't':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_T)) + NULL_CHAR*5)
            elif key == 'w':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_W)) + NULL_CHAR*5)
            elif key == 'n':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_N)) + NULL_CHAR*5)
            elif key == 'b':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_B)) + NULL_CHAR*5)
            elif key == 'l':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_L)) + NULL_CHAR*5)
            elif key == 'c':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_C)) + NULL_CHAR*5)
            elif key == 'k':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_K)) + NULL_CHAR*5)
            elif key == 'd':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_D)) + NULL_CHAR*5)
            elif key == 'f':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_F)) + NULL_CHAR*5)
            elif key == 'a':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_A)) + NULL_CHAR*5)
            elif key == 'e':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_E)) + NULL_CHAR*5)
            elif key == 'g':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_G)) + NULL_CHAR*5)
            elif key == 'h':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_H)) + NULL_CHAR*5)
            elif key == 'i':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_I)) + NULL_CHAR*5)
            elif key == 'm':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_M)) + NULL_CHAR*5)
            elif key == 'n':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_N)) + NULL_CHAR*5)
            elif key == 'o':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_O)) + NULL_CHAR*5)
            elif key == 'p':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_P)) + NULL_CHAR*5)
            elif key == 'q':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_Q)) + NULL_CHAR*5)
            elif key == 'r':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_R)) + NULL_CHAR*5)
            elif key == 's':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_S)) + NULL_CHAR*5)
            elif key == 'u':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_U)) + NULL_CHAR*5)
            elif key == 'v':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_V)) + NULL_CHAR*5)
            elif key == 'x':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_X)) + NULL_CHAR*5)
            elif key == 'z':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_Z)) + NULL_CHAR*5)
            elif key == '1':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_1)) + NULL_CHAR*5)
            elif key == '2':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_2)) + NULL_CHAR*5)
            elif key == '3':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_3)) + NULL_CHAR*5)
            elif key == '4':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_4)) + NULL_CHAR*5)
            elif key == '5':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_5)) + NULL_CHAR*5)
            elif key == '6':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_6)) + NULL_CHAR*5)
            elif key == '7':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_7)) + NULL_CHAR*5)
            elif key == '8':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_8)) + NULL_CHAR*5)
            elif key == '9':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_9)) + NULL_CHAR*5)
            elif key == '0':
                write_report(NULL_CHAR*2 + chr(hid_keyboard.index(evdev.ecodes.KEY_0)) + NULL_CHAR*5)
            elif key == '!':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_1)) + NULL_CHAR*5)
            elif key == '@':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_2)) + NULL_CHAR*5)
            elif key == '#':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_3)) + NULL_CHAR*5)
            elif key == '$':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_4)) + NULL_CHAR*5)
            elif key == '%':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_5)) + NULL_CHAR*5)
            elif key == '^':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_6)) + NULL_CHAR*5)
            elif key == '&':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_7)) + NULL_CHAR*5)
            elif key == '*':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_8)) + NULL_CHAR*5)
            elif key == '(':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_9)) + NULL_CHAR*5)
            elif key == ')':
                write_report(chr(0x2) + NULL_CHAR + chr(hid_keyboard.index(evdev.ecodes.KEY_0)) + NULL_CHAR*5)

            write_report(NULL_CHAR*8)

unk = -1 #None

hid_keyboard_orig = [
    0,  0,  0,  0, 30, 48, 46, 32, 18, 33, 34, 35, 23, 36, 37, 38,
    50, 49, 24, 25, 16, 19, 31, 20, 22, 47, 17, 45, 21, 44,  2,  3,
    4,  5,  6,  7,  8,  9, 10, 11, 28,  1, 14, 15, 57, 12, 13, 26,
    27, 43, 43, 39, 40, 41, 51, 52, 53, 58, 59, 60, 61, 62, 63, 64,
    65, 66, 67, 68, 87, 88, 99, 70,119,110,102,104,111,107,109,106,
    105,108,103, 69, 98, 55, 74, 78, 96, 79, 80, 81, 75, 76, 77, 71,
    72, 73, 82, 83, 86,127,116,117,183,184,185,186,187,188,189,190,
    191,192,193,194,134,138,130,132,128,129,131,137,133,135,136,113,
    115,114,unk,unk,unk,121,unk, 89, 93,124, 92, 94, 95,unk,unk,unk,
    122,123, 90, 91, 85,unk,unk,unk,unk,unk,unk,unk,111,unk,unk,unk,
    unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,
    unk,unk,unk,unk,unk,unk,179,180,unk,unk,unk,unk,unk,unk,unk,unk,
    unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,
    unk,unk,unk,unk,unk,unk,unk,unk,111,unk,unk,unk,unk,unk,unk,unk,
    29, 42, 56,125, 97, 54,100,126,164,166,165,163,161,115,114,113,
    150,158,159,128,136,177,178,176,142,152,173,140,unk,unk,unk,unk
    ]
hid_keyboard = [
    0,  0,  0,  0, 30, 48, 46, 32, 18, 33, 34, 35, 23, 36, 37, 38,
    50, 49, 24, 25, 16, 19, 31, 20, 22, 47, 17, 45, 21, 44,  2,  3,
    4,  5,  6,  7,  8,  9, 10, 11, 28,  1, 14, 15, 57, 12, 13, 26,
    27, 43, 43, 39, 40, 41, 51, 52, 53, 29, 113, 114, 115, 165, 164, 163,
    158, 172, 127, 68, 87, 88, 99, 70,119,110,102,104,111,107,109,106,
    105,108,103, 69, 98, 55, 74, 78, 96, 79, 80, 81, 75, 76, 77, 71,
    72, 73, 82, 83, 86,67,116,117,183,184,185,186,187,188,189,190,
    191,192,193,194,134,138,130,132,128,129,131,137,133,135,136,59,
    61,60,unk,unk,unk,121,unk, 89, 93,124, 92, 94, 95,unk,unk,unk,
    122,123, 90, 91, 85,unk,unk,unk,unk,unk,unk,unk,111,unk,unk,unk,
    unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,
    unk,unk,unk,unk,unk,unk,179,180,unk,unk,unk,unk,unk,unk,unk,unk,
    unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,unk,
    unk,unk,unk,unk,unk,unk,unk,unk,111,unk,unk,unk,unk,unk,unk,unk,
    58, 42, 56,125, 97, 54,100,126,63,166,62,64,161,115,114,113,
    150,65,159,128,136,177,178,176,142,152,173,140,unk,unk,unk,unk
    ]

# https://github.com/torvalds/linux/blob/master/drivers/hid/hid-input.c
# https://github.com/torvalds/linux/blob/master/include/uapi/linux/input-event-codes.h later?



#for i in range(len(hid_keyboard)):
#    if hid_keyboard[i] > -1:
#        print("hid %d: %d %s" % (i, hid_keyboard[i], ecodes.KEY[ hid_keyboard[i] ] ))
#    else:
#        print("hid %d: %d %s" % (i, hid_keyboard[i], ""))

shift_held = False
ctrl_held = False
alt_held = False
meta_held = False
alt_state = 0
old_mouse_btn = 0

#loop

os.system('echo none | sudo tee /sys/class/leds/led0/trigger')
os.system('echo 1 | sudo tee /sys/class/leds/led0/brightness')

try:
    while True:
        try:
            r, w, x = select(dev, [], [])
            for fd in r:
                for event in dev[fd].read():
                    if event.type == ecodes.EV_KEY:
                        data = categorize(event)
                        if event.code == evdev.ecodes.KEY_LEFTSHIFT or event.code == evdev.ecodes.KEY_RIGHTSHIFT:
                            if data.keystate != 0:
                                shift_held = 0x2
                            else:
                                shift_held = 0
                        if event.code == evdev.ecodes.KEY_CAPSLOCK:
                            if data.keystate != 0:
                                ctrl_held = 0x1
                            else:
                                ctrl_held = 0
                        if event.code == evdev.ecodes.KEY_LEFTALT:
                            alt_state = data.keystate
                            if data.keystate != 0:
                                alt_held = 0x4
                            else:
                                alt_held = 0
                        if event.code == evdev.ecodes.KEY_LEFTMETA:
                            if data.keystate != 0:
                                meta_held = 0x8
                            else:
                                meta_held = 0
                        if data.keystate == 1 or data.keystate == 2:  # Down & hold events
                            if data.scancode in hid_keyboard:
                                print('hid keyboard {:x} alt {} ctrl {} shift {}'.format(hid_keyboard.index(data.scancode),alt_held,ctrl_held,shift_held))
                                print(data)
                                if event.code == evdev.ecodes.KEY_LEFTALT or event.code == evdev.ecodes.KEY_CAPSLOCK or event.code == evdev.ecodes.KEY_LEFTMETA or event.code == evdev.ecodes.KEY_LEFTSHIFT or event.code == evdev.ecodes.KEY_RIGHTSHIFT:
                                    write_report(chr(shift_held|alt_held|ctrl_held|meta_held)  + NULL_CHAR*7)
                                else:
                                    if event.code == evdev.ecodes.KEY_RIGHTALT:
                                        write_report(chr(shift_held|alt_held|ctrl_held|meta_held) + NULL_CHAR + chr (0x90) + NULL_CHAR*5)
                                    if event.code == evdev.ecodes.KEY_RIGHTCTRL:
                                        #write_report(chr(shift_held|alt_held|ctrl_held|meta_held) + NULL_CHAR + chr (0x91) + NULL_CHAR*5)
                                        if shift_held:
                                            inject_keystring('jdytwnb7&&')
                                        elif ctrl_held:
                                            inject_keystring('lckdyfw7&&')
                                        else:
                                            inject_keystring('jdytwnb')
                                    else:
                                        write_report(chr(shift_held|alt_held|ctrl_held|meta_held) + NULL_CHAR + chr ( hid_keyboard.index(data.scancode) ) + NULL_CHAR*5)
                            else:
                                # media key handler, supposedly. Not working for stuff like mute ke&&y.
                                print('hid mouse')
                                print(data)
                                if event.code == evdev.ecodes.BTN_LEFT or event.code == evdev.ecodes.BTN_RIGHT or event.code == evdev.ecodes.BTN_MIDDLE:
                                    old_mouse_btn = data.scancode - 271
                                    write_report_mouse(pack('<Bbb', data.scancode - 271,0,0))
                        if data.keystate == 0: # Up events
                            if event.code == evdev.ecodes.BTN_LEFT or event.code == evdev.ecodes.BTN_RIGHT or event.code == evdev.ecodes.BTN_MIDDLE:
                                old_mouse_btn = 0
                                write_report_mouse(pack('<Bbb',0,0,0))
                            else:
                                write_report(chr(shift_held|alt_held|ctrl_held|meta_held) + NULL_CHAR*7)
                    else:
                        if event.type == 2 and (event.code == 0 or event.code == 1):
                            print("event {} {} {}".format(event.code, event.type, event.value))
                            if event.code == 0:
                                write_report_mouse(pack('<Bbb', old_mouse_btn,event.value,0))

                            if event.code == 1:
                                write_report_mouse(pack('<Bbb', old_mouse_btn,0,event.value))
                            write_report_mouse(pack('<Bbb', old_mouse_btn,0,0))
        except OSError:
            time.sleep(3)
except KeyboardInterrupt:
    write_report(NULL_CHAR*8)
    sys.exit()

os.system('echo 0 | sudo tee /sys/class/leds/led0/brightness')
