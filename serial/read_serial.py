# Reads Serial
import serial


def serial_connection(port, baudrate):
    try:
        stream = serial.Serial(port=port, baudrate=baudrate)
        b_buffer = stream.readline()
        return b_buffer.decode("ascii")
    except:
        print("Couldn't connect with serial port")
        return "_E_"


# Test to check validation of approach
if __name__ == "__main__":
    while True:
        # Don't forget to change the port path
        buffer = serial_connection(port="", baudrate=115200)
        print(buffer)
        if "\033" in buffer:
            print("Found escape character for ANSI pattern")
        if "\033[1;31m" in buffer:
            print("Found Error Code: {}".format(buffer))
        if "Last reset cause:" in buffer:
            print("Found Reset condition")
        else:
            print("Found nothing")
