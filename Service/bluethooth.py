import serial
ser = serial.Serial('COM4', 9800, timeout=1)
ser.write(b'Hello')