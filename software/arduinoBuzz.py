import time
import serial

arduino = serial.Serial('/dev/ttyACM0', 115200)
if arduino.isOpen():
    arduino.close()
arduino.open()

def writeBuzz(freq, pose):
    print("{freq}|{pose}".format(freq=freq, pose=pose))
    freq = abs(freq)
    arduino.write(f"{freq}|{pose}".encode())

def buzzLeft(freq):
    writeBuzz(freq, 0)

def buzzRight(freq):
    writeBuzz(freq, 1)

def buzzAll(freq):
    writeBuzz(freq, -1)
