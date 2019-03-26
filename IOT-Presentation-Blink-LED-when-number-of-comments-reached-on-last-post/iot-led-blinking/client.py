from flask import Flask, request

import serial

from sys import exit
from subprocess import getoutput
import re

class colors:
    GREEN = "\u001b[32m"
    RESET = "\u001b[0m"
    RED = "\u001b[31m"
    YELLOW = "\u001b[33m"

app = Flask(__name__)

ser = None
@app.before_first_request
def check_adruino():
    global ser

    try:
        output = getoutput("python -m serial.tools.list_ports")
        m = re.match("(/dev/tty[A0-Z9]*).*", output, re.MULTILINE)
        if m:
            port = m.group(1)
            print(colors.YELLOW + 'Arduino is connected to ' + port + colors.RESET + "\n")
            ser = serial.Serial(port, 9600)
        else:
            print("Check your Arduino connection.")
            exit(1)
    except Exception as e:
        print(str(e))
        exit(1)



@app.route('/', methods=['GET'])
def get_notification():
    data = bytes(request.args.get('not'), encoding="utf-8")
    print(data)
    if data == b'1':
        print(colors.GREEN +"LED is on" + colors.RESET)
    else:
        print(colors.RED +"LED is off" + colors.RESET)
    ser.write(data)
    return 'ok', 200

if __name__ == "__main__":
    check_adruino()
    app.run(debug=True, port=8000)
