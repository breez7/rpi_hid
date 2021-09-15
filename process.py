
#!/usr/bin/env python3

import evdev, time
from evdev import InputDevice, categorize, ecodes
import asyncio

import io
from select import select
import os
import sys
from struct import pack

import threading
import signal

from game_pad import XBOXGamepad
from game_pad import XBOXButton
from game_pad import DPad

from collections import defaultdict

tesla = os.path.isfile('/backingfiles/music_disk.bin')
gamepad = XBOXGamepad()
gamepad.begin('/dev/hidg0')

EVENT2BUTTON = defaultdict(lambda:XBOXButton.DUMMY)
EVENT2BUTTON[ecodes.KEY_J] = XBOXButton.A
EVENT2BUTTON[ecodes.KEY_K] = XBOXButton.B
EVENT2BUTTON[ecodes.KEY_U] = XBOXButton.X
EVENT2BUTTON[ecodes.KEY_I] = XBOXButton.Y
EVENT2BUTTON[ecodes.KEY_H] = XBOXButton.LT
EVENT2BUTTON[ecodes.KEY_L] = XBOXButton.RT
EVENT2BUTTON[ecodes.KEY_Y] = XBOXButton.L3
EVENT2BUTTON[ecodes.KEY_O] = XBOXButton.R3
EVENT2BUTTON[ecodes.KEY_EQUAL] = XBOXButton.START
EVENT2BUTTON[ecodes.KEY_MINUS] = XBOXButton.BACK

EVENT2BUTTON[ecodes.BTN_LEFT] = XBOXButton.A
EVENT2BUTTON[ecodes.BTN_RIGHT] = XBOXButton.B
EVENT2BUTTON[ecodes.BTN_MIDDLE] = XBOXButton.X

EVENT2BUTTON[ecodes.BTN_A] = XBOXButton.A
EVENT2BUTTON[ecodes.BTN_B] = XBOXButton.B
EVENT2BUTTON[ecodes.BTN_X] = XBOXButton.X
EVENT2BUTTON[ecodes.BTN_Y] = XBOXButton.Y
EVENT2BUTTON[ecodes.BTN_START] = XBOXButton.START
EVENT2BUTTON[ecodes.BTN_SELECT] = XBOXButton.BACK
EVENT2BUTTON[ecodes.BTN_TL] = XBOXButton.LT
EVENT2BUTTON[ecodes.BTN_TR] = XBOXButton.RT
EVENT2BUTTON[ecodes.BTN_THUMBL] = XBOXButton.L3
EVENT2BUTTON[ecodes.BTN_THUMBR] = XBOXButton.R3

EVENT2FUNC = defaultdict(lambda:gamepad.dummy)
EVENT2FUNC[ecodes.REL_X] = gamepad.leftXAxis
EVENT2FUNC[ecodes.REL_Y] = gamepad.leftYAxis
EVENT2FUNC[ecodes.REL_WHEEL] = gamepad.leftZAxis
EVENT2FUNC[ecodes.REL_HWHEEL] = gamepad.rightZAxis

EVENT2FUNC[ecodes.KEY_N] = gamepad.leftZAxis
EVENT2FUNC[ecodes.KEY_M] = gamepad.rightZAxis

EVENT2FUNC[ecodes.ABS_X] = gamepad.leftXAxis
EVENT2FUNC[ecodes.ABS_Y] = gamepad.leftYAxis
EVENT2FUNC[ecodes.ABS_RX] = gamepad.rightXAxis
EVENT2FUNC[ecodes.ABS_RY] = gamepad.rightYAxis
EVENT2FUNC[ecodes.ABS_Z] = gamepad.leftZAxis
EVENT2FUNC[ecodes.ABS_RZ] = gamepad.rightZAxis

# up down left right
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
DIRECTION_KEYS = defaultdict(lambda:UP)
DIRECTION_KEYS[ecodes.KEY_W] = UP
DIRECTION_KEYS[ecodes.KEY_A] = LEFT
DIRECTION_KEYS[ecodes.KEY_S] = DOWN
DIRECTION_KEYS[ecodes.KEY_D] = RIGHT

DIRECTION_STATE = [False, False, False, False]

def get_direction():
    if DIRECTION_STATE[UP] and DIRECTION_STATE[RIGHT]:
        return DPad.UP_RIGHT
    elif DIRECTION_STATE[UP] and DIRECTION_STATE[LEFT]:
        return DPad.UP_LEFT
    elif DIRECTION_STATE[DOWN] and DIRECTION_STATE[RIGHT]:
        return DPad.DOWN_RIGHT
    elif DIRECTION_STATE[DOWN] and DIRECTION_STATE[LEFT]:
        return DPad.DOWN_LEFT
    elif DIRECTION_STATE[UP]:
        return DPad.UP
    elif DIRECTION_STATE[DOWN]:
        return DPad.DOWN
    elif DIRECTION_STATE[LEFT]:
        return DPad.LEFT
    elif DIRECTION_STATE[RIGHT]:
        return DPad.RIGHT
    else:
        return DPad.CENTERED


first = True
dev = {}

os.system('echo none | sudo tee /sys/class/leds/led0/trigger')
os.system('echo 0 | sudo tee /sys/class/leds/led0/brightness')
NULL_CHAR = chr(0)
is_exit = False
def write_report(report):
    with open('/dev/hidg2', 'rb+') as fd:
        fd.write(bytes(report, encoding='utf8'))
def write_report_mouse(report):
    with open('/dev/hidg1', 'rb+') as fd:
        fd.write(report)

def write_report_gamepad():
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report)

def signal_handler(s, frmae):
    if s == signal.SIGABRT or s== signal.SIGHUP or  s == signal.SIGINT or s == signal.SIGTERM or s == signal.SIGSEGV :
        os.system('echo 0 | sudo tee /sys/class/leds/led0/brightness')
        is_exit = True  
        print('signal {}'.format(s))
        write_report(NULL_CHAR*8)
        sys.exit()


signal.signal(signal.SIGABRT, signal_handler)
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGSEGV, signal_handler)
#signal.signal(signal.SIGKILL, signal_handler)
signal.signal(signal.SIGHUP, signal_handler)

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

#            print("#find")
#            print(devices)
            dev_paths = [temp.path for temp in dev.values()]
#            print(dev_paths)
            for device in devices:
                if device in dev_paths:
                    continue
                if first == False:
                    kill()
                    return
                a = InputDevice(device)
                dev[a.fd] = a
                # a.grab()
                print("!!!!!!add")
                if is_exit == False:
                    os.system('echo 1 | sudo tee /sys/class/leds/led0/brightness')
#            print("###find")
            dev_paths = [temp.path for temp in dev.values()]
#            print(dev_paths)
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
#config = {}
#with open(os.path.dirname(os.path.abspath(__file__)) + "/config.conf") as f:
#    for line in f:
#        name, var = line.partition("=")[::2]
#        config[name.strip()] = var.lower().strip().strip('\"')
#
#
#
#print (config["devicename"])

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
mouse_middle_held = False


async def keyboard_handle_events(device):
    global shift_held, ctrl_held, alt_held, meta_held, alt_state, old_mouse_btn, mouse_middle_held
    with device.grab_context():
        async for event in device.async_read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                if mouse_middle_held:
                    if data.keystate == 1:
                        if event.code == ecodes.KEY_J:
                            write_report_mouse(pack('<Bbbb', 1 << 3 ,0,0,0))
                        elif event.code == ecodes.KEY_K:
                            write_report_mouse(pack('<Bbbb', 1 << 4 ,0,0,0))
                    elif data.keystate == 0:
                            write_report_mouse(pack('<Bbbb', 0,0,0,0))
                    continue
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
#                                print('hid keyboard {:x} alt {} ctrl {} shift {}'.format(hid_keyboard.index(data.scancode),alt_held,ctrl_held,shift_held))
#                                print(data)
                        if event.code == evdev.ecodes.KEY_LEFTALT or event.code == evdev.ecodes.KEY_CAPSLOCK or event.code == evdev.ecodes.KEY_LEFTMETA or event.code == evdev.ecodes.KEY_LEFTSHIFT or event.code == evdev.ecodes.KEY_RIGHTSHIFT:
                            write_report(chr(shift_held|alt_held|ctrl_held|meta_held)  + NULL_CHAR*7)
                        else:
                            if event.code == evdev.ecodes.KEY_RIGHTALT:
                                write_report(chr(shift_held|alt_held|ctrl_held|meta_held) + NULL_CHAR + chr (0x90) + NULL_CHAR*5)
                            elif event.code == evdev.ecodes.KEY_RIGHTCTRL:
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
                        print('not support key {}'.format(str(event)))
                elif data.keystate == 0: # Up events
                    write_report(chr(shift_held|alt_held|ctrl_held|meta_held) + NULL_CHAR*7)

async def mouse_handle_events(device):
    global shift_held, ctrl_held, alt_held, meta_held, alt_state, old_mouse_btn, mouse_middle_held
    with device.grab_context():
        async for event in device.async_read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                if data.keystate == 1 or data.keystate == 2:  # Down & hold events
                    if event.code == evdev.ecodes.BTN_MIDDLE:
                        print('m hlod')
                        mouse_middle_held = True
                    else:
                        if event.code == evdev.ecodes.BTN_LEFT:
                            old_mouse_btn = 1 
                        elif event.code == evdev.ecodes.BTN_RIGHT:
                            old_mouse_btn = 1 << 1
                        elif event.code == evdev.ecodes.BTN_FORWARD or \
                            event.code == evdev.ecodes.BTN_EXTRA:
                            old_mouse_btn = 1 << 4
                        elif event.code == evdev.ecodes.BTN_BACK or \
                            event.code == evdev.ecodes.BTN_SIDE:
                            old_mouse_btn = 1 << 3
                        write_report_mouse(pack('<Bbbb', old_mouse_btn,0,0,0))
                elif data.keystate == 0: # Up events
                    if event.code == evdev.ecodes.BTN_MIDDLE:
                        print('m unhlod')
                        mouse_middle_held = False
                    old_mouse_btn = 0
                    write_report_mouse(pack('<Bbbb',0,0,0,0))
            elif event.type == ecodes.EV_REL:
                if event.code == ecodes.REL_X:
                    write_report_mouse(pack('<Bbbb', old_mouse_btn,event.value,0,0))
                elif event.code == ecodes.REL_Y:
                    write_report_mouse(pack('<Bbbb', old_mouse_btn,0,event.value,0))
                elif event.code == ecodes.REL_HWHEEL:
                    pass
                elif event.code == ecodes.REL_WHEEL:
                    write_report_mouse(pack('<Bbbb', old_mouse_btn,0,0,event.value))
                write_report_mouse(pack('<Bbbb', old_mouse_btn,0,0,0))

async def gamepad_from_keyboard_mouse_handle_events(device):
    global shift_held, ctrl_held, alt_held, meta_held, alt_state, old_mouse_btn, gamepad
    right_throttle = 0
    left_throttle =0
    global up,down,left,right
    with device.grab_context():
        async for event in device.async_read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                print('ev_key {} {}'.format(event, data))
                if data.keystate == 1 or data.keystate ==2:
                    if event.code in DIRECTION_KEYS.keys():
                        DIRECTION_STATE[DIRECTION_KEYS[event.code]] = True
                        gamepad.press_dpad(get_direction())
                    elif event.code == ecodes.KEY_N:
                        left_throttle += 10
                        EVENT2FUNC[event.code](left_throttle)
                    elif event.code == ecodes.KEY_M:
                        right_throttle += 10
                        EVENT2FUNC[event.code](right_throttle)
                    else:
                        gamepad.press(EVENT2BUTTON[event.code])
                elif data.keystate == 0:
                    if event.code in DIRECTION_KEYS.keys():
                        DIRECTION_STATE[DIRECTION_KEYS[event.code]] = False
                        gamepad.press_dpad(get_direction())
                    elif event.code == ecodes.KEY_N:
                        left_throttle = 0
                        EVENT2FUNC[event.code](left_throttle)
                    elif event.code == ecodes.KEY_M:
                        right_throttle = 0
                        EVENT2FUNC[event.code](right_throttle)
                    else:
                        gamepad.release(EVENT2BUTTON[event.code])
            elif event.type == ecodes.EV_REL:
                print('ev_rel {} '.format(event))
                if event.code == ecodes.REL_WHEEL:
                    left_throttle += event.value * 10
                    event.value = left_throttle
                elif event.code == ecodes.REL_HWHEEL:
                    right_throttle += event.value * 10
                    event.value = right_throttle

                EVENT2FUNC[event.code](event.value)

async def gamepad_handle_events(device):
    global shift_held, ctrl_held, alt_held, meta_held, alt_state, old_mouse_btn, gamepad
    with device.grab_context():
        async for event in device.async_read_loop():
            if event.type == ecodes.EV_KEY:
                data = categorize(event)
                print('ev_key {} {}'.format(event, data))
                if data.keystate == 1 or data.keystate ==2:
                    gamepad.press(EVENT2BUTTON[event.code])
                elif data.keystate == 0:
                    gamepad.release(EVENT2BUTTON[event.code])
            elif event.type == ecodes.EV_REL:
                print('ev_rel {} '.format(event))
                EVENT2FUNC[event.code](event.value)


#loop
time.sleep(2)
for key in dev.keys():
    print(dev[key].capabilities(verbose=True))
    print('########################')
    if evdev.ecodes.EV_KEY in dev[key].capabilities():
        if evdev.ecodes.KEY_A in dev[key].capabilities()[evdev.ecodes.EV_KEY]:
            print('keyboard'), dev[key]
            if tesla:
                asyncio.ensure_future(gamepad_from_keyboard_mouse_handle_events(dev[key]))
            else:
                asyncio.ensure_future(keyboard_handle_events(dev[key]))
        elif evdev.ecodes.KEY_SEARCH in dev[key].capabilities()[evdev.ecodes.EV_KEY]:
            print('media key'), dev[key]
            asyncio.ensure_future(keyboard_handle_events(dev[key]))
        elif evdev.ecodes.BTN_MOUSE in dev[key].capabilities()[evdev.ecodes.EV_KEY]:
            print('mouse'), dev[key]
            if tesla:
                asyncio.ensure_future(gamepad_from_keyboard_mouse_handle_events(dev[key]))
            else:
                asyncio.ensure_future(mouse_handle_events(dev[key]))
        elif evdev.ecodes.BTN_START in dev[key].capabilities()[evdev.ecodes.EV_KEY]:
            print('xbox gamepad'), dev[key]
            asyncio.ensure_future(gamepad_handle_events(dev[key]))

loop = asyncio.get_event_loop()
loop.run_forever()
        


