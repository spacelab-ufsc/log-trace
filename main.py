# SCRIPT TO RUN

import time 
import config
import log_handlers.log_handler as log
import serial.read_serial as sr

# Reference day as an int, needed for generating files
ref_day = int(time.strftime("%d")) 
# Reference date, needed for generating files
ref_date = time.strftime("[%d/%m/%Y]")
# Initial File for log storage
# TODO Choose the file dynamics
#try:
    #path = ("{}/log-{}.txt".format(config.PATH_FOR_LOGS,ref_date))
    #file = open(path,"a+")
#except FileNotFoundError:
     # TODO: Fix the generic exception 
#    print("Error: FileNotFoundError -> Probably a something wrong with the path")

# TEST
file = open("a.txt","a+")
file.write("SUCESS")

while True:
    # Start reading Serial Port
    buffer = sr.serial_connection(port=config.PORT_EPS,bauldrate=config.BAUDRATE,parity=config.PARITY,stopbit=config.STOP_BIT)
    # Match each case for logging
    (code,message) = log.log_handler(buffer)
    # Base case, didn't matched any case
    if code == "Ok":
        continue
    # Matched a reading
    else:
        # Current time 
        date = time.strftime("[%d/%m/%Y] - %H:%M:%S")

        # Current day as an int
        current_day = int(time.strftime("%d")) 

        # Checks if the day changed and creates a new file if it has changed
        if ref_day != current_day:
            ref_day = current_day
            ref_date = time.strftime("[%d/%m/%Y]")
            try:
                file.close()
                path = ("{}/log-{}.txt".format(config.PATH_FOR_LOGS,ref_date))
                file = open(path,"a+")
            except:
                # TODO: Fix the generic exception 
                print("Error either on closing the file or creating a new one")
        
        # TODO Write the log contents to the file
        #file.write(processed_buffer)

