import serial

ser = serial.Serial('/dev/ttyACM1', 9600)

while True:
    data = input('1 => led on, 0 => led off ?: ' )
    if (data == '-1'):
        ser.write(b'0')
        break
    data = bytes(data, encoding='utf8')
    ser.write(data)
