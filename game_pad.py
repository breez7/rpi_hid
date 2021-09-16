#!/usr/bin/env python3

from struct import pack
import array
import threading
from enum import IntEnum

# Direction pad names
class DPad(IntEnum):
    """DPad direction names"""
    CENTERED = 0xF
    UP = 0
    UP_RIGHT = 1
    RIGHT = 2
    DOWN_RIGHT = 3
    DOWN = 4
    DOWN_LEFT = 5
    LEFT = 6
    UP_LEFT = 7

class DPad_XBOX(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

# Button names
class XBOXButton(IntEnum):
    Y = 0
    B = 1
    A = 2
    X = 3
    LT = 4
    RT = 5
    L3 = 6
    R3 = 7
    BACK = 8
    START = 9
    DUMMY = 10

class NSButton(IntEnum):
    """NSButton names based on Nintendo Switch buttons"""
    Y = 0
    B = 1
    A = 2
    X = 3
    LEFT_TRIGGER = 4
    RIGHT_TRIGGER = 5
    LEFT_THROTTLE = 6
    RIGHT_THROTTLE = 7
    MINUS = 8
    PLUS = 9
    LEFT_STICK = 10
    RIGHT_STICK = 11
    HOME = 12
    CAPTURE = 13

class DS4Button(IntEnum):
    """Button names based on Dual Shock 4 PS4 buttons"""
    SQUARE = 0
    CROSS = 1
    CIRCLE = 2
    TRIANGLE = 3
    L1 = 4
    R1 = 5
    L2 = 6
    R2 = 7
    SHARE = 8
    OPTIONS = 9
    L3 = 10
    R3 = 11
    LOGO = 12
    TPAD = 13

class XBOXGamepad():
    compass_dir_x = array.array('B', \
            [0, 0, 128, 255, 255, 255, 128, 0, \
            128, 128, 128, 128, 128, 128, 128, 128, 128])
    compass_dir_y = array.array('B', \
            [128, 255, 255, 255, 128, 0, 0, 0,\
            128, 128, 128, 128, 128, 128, 128, 128, 128])


    def __init__(self):
        self.thread_lock = threading.Lock()
        self.left_x_axis = 128
        self.left_y_axis = 128
        self.right_x_axis = 128
        self.right_y_axis = 128
        self.left_z_axis = 0
        self.right_z_axis = 0
        self.my_buttons = 0
        self.d_pad = DPad.CENTERED

    def begin(self, devname):
        with self.thread_lock:
            self.devhandle = open(devname, 'wb+')
            self.left_x_axis = 128 
            self.left_y_axis = 128
            self.right_x_axis = 128
            self.right_y_axis = 128
            self.left_z_axis = 0
            self.right_z_axis = 0
            self.my_buttons = 0
            self.d_pad = DPad.CENTERED
            self.write()
        return

    def end(self):
        self.devhandle.close()
        return

    def write(self):
        self.devhandle.write(pack('<HBBBBBBBB',
            self.my_buttons, self.d_pad,
            self.left_x_axis, self.left_y_axis, \
            self.right_x_axis, self.right_y_axis, \
            self.left_z_axis, self.right_z_axis, 0))
        self.devhandle.flush()
        return

    def press_dpad(self, direction):
        with self.thread_lock:
            print(direction)
            self.d_pad = direction
            self.write()
        return

    def release_dpad(self, button_number):
        self.d_pad = DPad.CENTERED
        return

    def press(self, button_number):
        """Press button 0..9"""
        if button_number == XBOXButton.DUMMY:
            print('not supported button')
            return
        if button_number < 0:
            button_number = 0
        if button_number > 9:
            button_number = 9 
        with self.thread_lock:
            self.my_buttons |= (1<<button_number)
            self.write()
        return

    def release(self, button_number):
        """Release button 0..3"""
        if button_number == XBOXButton.DUMMY:
            return
        if button_number < 0:
            button_number = 0
        if button_number > 9:
            button_number = 9 
        with self.thread_lock:
            self.my_buttons &= ~(1<<button_number)
            self.write()
        return

    def releaseAll(self):
        """Release all buttons"""
        with self.thread_lock:
            self.my_buttons = 0
            self.write()
        return

    def buttons(self, buttons):
        """Set all buttons 0..9"""
        with self.thread_lock:
            self.my_buttons = buttons & 0x3ff
            self.write()
        return

    def dummy(self, position):
        pass
    def leftXAxis(self, position):
        """Move left stick X axis 0..128..255"""
        # position += self.left_x_axis
        if position < 0:
            position = 0
        if position > 255:
            position = 255
        with self.thread_lock:
            self.left_x_axis = position
            self.write()
        return

    def leftYAxis(self, position):
        """Move left stick Y axis 0..128..255"""
        # position += self.left_y_axis
        if position < 0:
            position = 0
        if position > 255:
            position = 255
        with self.thread_lock:
            self.left_y_axis = position
            self.write()
        return

    def rightXAxis(self, position):
        """Move right stick X axis 0..128..255"""
        # position += self.right_x_axis
        if position < 0:
            position = 0
        if position > 255:
            position = 255
        with self.thread_lock:
            self.right_x_axis = position
            self.write()
        return

    def rightYAxis(self, position):
        """Move right stick Y axis 0..128..255"""
        # position += self.right_y_axis
        if position < 0:
            position = 0
        if position > 255:
            position = 255
        with self.thread_lock:
            self.right_y_axis = position
            self.write()
        return

    def leftZAxis(self, position):
        # position += self.left_z_axis
        if position < 0:
            position = 0
        if position > 255:
            position = 255
        with self.thread_lock:
            self.left_z_axis = position
            self.write()
        return

    def rightZAxis(self, position):
        # position += self.right_z_axis
        if position < 0:
            position = 0
        if position > 255:
            position = 255
        with self.thread_lock:
            self.right_z_axis = position
            self.write()
        return

def main():
    """ test NSGamepad class """
    import time

    gamepad = NSGamepad()
    gamepad.begin('/dev/hidg0')

    while True:
        # Press and hold every button 0..13
        for button in range(0, 14):
            gamepad.press(button)
            time.sleep(0.1)
        time.sleep(1)
        # Release all buttons
        gamepad.releaseAll()
        time.sleep(1)
        # Press all 14 buttons at the same time
        gamepad.buttons(0x3fff)
        time.sleep(1)
        # Release all buttons
        gamepad.releaseAll()
        time.sleep(1)
        # Move directional pad in all directions
        # 0 = North, 1 = North-East, 2 = East, etc.
        for direction in range(0, 8):
            gamepad.dPad(direction)
            time.sleep(0.5)
        # Move directional pad to center
        gamepad.dPad(DPad.CENTERED)

        # Move the left stick then right stick
        stick = [
            {"x": 128, "y": 128},
            {"x": 128, "y": 0},
            {"x": 255, "y": 0},
            {"x": 255, "y": 128},
            {"x": 255, "y": 255},
            {"x": 128, "y": 255},
            {"x":   0, "y": 255},
            {"x":   0, "y": 128},
            {"x":   0, "y":   0},
            {"x": 128, "y": 128},
        ]
        for direction in range(0, 10):
            gamepad.leftXAxis(stick[direction]['x'])
            gamepad.leftYAxis(stick[direction]['y'])
            time.sleep(0.5)
        for direction in range(0, 10):
            gamepad.rightXAxis(stick[direction]['x'])
            gamepad.rightYAxis(stick[direction]['y'])
            time.sleep(0.5)

if __name__ == "__main__":
    main()
