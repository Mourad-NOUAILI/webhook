import requests
from time import sleep

import serial

from sys import exit
from subprocess import getoutput
import re

class colors:
    GREEN = "\u001b[32m"
    RESET = "\u001b[0m"
    RED = "\u001b[31m"
    YELLOW = "\u001b[33m"


def display(s, data, status):
    if not s[data][1]:
        if status == 'on':
            print(colors.GREEN +"LED is " + s[data][0] + colors.RESET)
        if status == 'off':
            print(colors.RED +"LED is " + s[data][0] + colors.RESET)

        s[data] = (s[data][0], True)

#####################################################################
output = getoutput("python -m serial.tools.list_ports")

m = re.match("(/dev/tty[A0-Z9]*).*", output, re.MULTILINE)
if m:
    print("[CTRL-C] to quit.\n")
    port = m.group(1)
    print(colors.YELLOW + 'Arduino is connected to ' + port + colors.RESET + "\n")
    ser = serial.Serial(port, 9600)
    d_prev = 'a'
    try:
        while True:
            r = requests.post("https://iot-bot-led-blink.herokuapp.com")
            d = r.text
            if not d == '0' and not d == '1':
                d = '0'
            if not d_prev == d:
                s = {'0': ('off', False), '1': ('on', False)}
            d_prev = d
            if d == '0' or d == '1':
                display(s, d, s[d][0])

                d = bytes(d, encoding='utf8')
                ser.write(d)
            else:
                if not s[d][1]:
                    display(s, d, s[d][0])
    except KeyboardInterrupt:
        print("\nProgram interrup by user.")
        exit(0)
else:
    print("Check your Arduino connection.")
