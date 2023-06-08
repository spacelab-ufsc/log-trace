# Reads Serial
import serial

def serial_connection(port,bauldrate,stopbit,parity):
    try:
        stream = serial.Serial(port=port,baudrate=bauldrate,stopbits=stopbit,parity=parity)
        b_buffer = stream.readline()
        return b_buffer.decode("ascii")
    except:
        # TODO Look for especific exceptions
        print("Couldn't connect with serial port")
