import time
import serial

arduino = serial.Serial('/dev/ttyACM0', 9600)
if arduino.isOpen():
    arduino.close()
arduino.open()

def writeBuzz(freq, pose):
    freq = abs(freq)
    arduino.write(f"{freq}|{pose}".encode())
    time.sleep(0.2)

def buzzLeft(freq):
    writeBuzz(freq, 0)

def buzzRight(freq):
    writeBuzz(freq, 1)

def buzzAll(freq):
    writeBuzz(freq, -1)
