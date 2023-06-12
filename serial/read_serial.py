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
        return "_"


if __name__ == "__main__":
    while True:
        buffer = serial_connection(port='',bauldrate=9600,stopbit=1,parity=0)
        print(buffer)
        if buffer.__contains__("\033"):
            print("Found escape character for ANSI patern")
        if buffer.__contains__( "\033[31;1;"):
            print("Found Error Code: {}".format(buffer))
