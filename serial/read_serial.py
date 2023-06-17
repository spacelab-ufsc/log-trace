# Reads Serial
import serial

def serial_connection(port,bauldrate):
    try:
        stream = serial.Serial(port=port,baudrate=bauldrate)
        b_buffer = stream.readline()
        return b_buffer.decode("ascii")
    except:
        # TODO Look for especific exceptions
        print("Couldn't connect with serial port")
        return "_E_"


# Test to check validation of approach
if __name__ == "__main__":
    while True:
        # Don't forget to change the port path
        buffer = serial_connection(port='',bauldrate=115200)
        print(buffer)
        if buffer.__contains__("\033"):
            print("Found escape character for ANSI pattern")
        if buffer.__contains__("\033[1;31m"):
            print("Found Error Code: {}".format(buffer))
        if buffer.__contains__("Last reset cause:"):
            print("Found Reset condition")
