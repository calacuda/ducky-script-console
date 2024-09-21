import time
import board
# from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
import busio
import json


kbd = Keyboard(usb_hid.devices)
cc = ConsumerControl(usb_hid.devices)
# uart = busio.UART(board.TX, board.RX, baudrate=9600)
# time.sleep(10)
uart = busio.UART(board.GP4, board.GP5, baudrate=115200)

DEFAULT_DELAY = 0.001

SPECIAL_KEYS = {
    "LeftSuper": Keycode.GUI,
    "RightSuper": Keycode.GUI,
    "Enter": Keycode.ENTER,
    "LeftShift": Keycode.SHIFT,
    "RightShift": Keycode.SHIFT,
    # TODO: add the rest.
}

SPECIAL_CHARS = {
    " ": (Keycode.SPACE,),
    "-": (Keycode.MINUS,),
    "\'": (Keycode.QUOTE,),
    "\"": (Keycode.SHIFT, Keycode.QUOTE),
    ".": (Keycode.PERIOD,),
    "\\": (Keycode.BACKSLASH,),
    "/": (Keycode.FORWARD_SLASH,),
    ":": (Keycode.SHIFT, Keycode.SEMICOLON),
    "&": (Keycode.SHIFT, Keycode.SEVEN),
    "?": (Keycode.SHIFT, Keycode.FORWARD_SLASH),
    "=": (Keycode.EQUALS,),
    "1": (Keycode.ONE,),
    "2": (Keycode.TWO,),
    "3": (Keycode.THREE,),
    "4": (Keycode.FOUR,),
    "5": (Keycode.FIVE,),
    "6": (Keycode.SIX,),
    "7": (Keycode.SEVEN,),
    "8": (Keycode.EIGHT,),
    "9": (Keycode.NINE,),
    "0": (Keycode.ZERO,),
    # TODO: add the rest.
}

# kbd.press(Keycode.GUI, Keycode.ENTER)
# kbd.release(Keycode.GUI, Keycode.ENTER)

# print(dir(uart))
# print(dir(Keycode))


def read_cmd():
    # TODO: make it read line instead of read
    # print("reading cmd")
    data = ""

    while True:
        char = uart.read(1)

        if char:
            # print(type(char), char)
            data += char.decode("ascii")

            if data.count("{") == data.count("}"):
                cmd = json.loads(data)
                # print("cmd : ", cmd)
                # print("data : ", data)

                return cmd


def hold_key(key):
    keycode = SPECIAL_KEYS.get(key)

    if keycode is None:
        print(f"ERROR: unknown keycode {key}")
        return

    kbd.press(keycode)


def release_key(key):
    keycode = SPECIAL_KEYS.get(key)

    if keycode is None:
        print(f"ERROR: unknown keycode {key}")
        return

    kbd.release(keycode)


def type_char(char):
    char = chr(char)

    if char.isupper():
        hold_key("LeftShift")

    try:
        key = (getattr(Keycode, char.upper()),)
    except AttributeError:
        key = SPECIAL_CHARS.get(char)

    kbd.press(*key)
    time.sleep(DEFAULT_DELAY)
    kbd.release(*key)

    if char.isupper():
        release_key("LeftShift")


def trigger_key(key):
    hold_key(key)
    time.sleep(DEFAULT_DELAY)
    release_key(key)


def led(state):
    """do led stuff"""
    pass


CASES = {
    "HoldKey": hold_key,
    "ReleaseKey": release_key,
    "TypeChar": type_char,
    "TriggerKey": trigger_key,
    "LED": led,
}


while True:
    cmd = list(read_cmd().items())[0]

    # print(cmd)
    switch = cmd[0]

    case = CASES.get(switch)

    if case is not None:
        case(cmd[1])
