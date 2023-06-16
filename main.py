# SCRIPT TO RUN

import time 
import config
import log_handlers.log_handler as log
import serial.read_serial as sr


while True:
    # Start reading Serial Port for all modules
    buffer_ttic = sr.serial_connection(port=config.PORT_TTIC,bauldrate=config.BAUDRATE)
    buffer_obdh = sr.serial_connection(port=config.PORT_OBDH,bauldrate=config.BAUDRATE)
    buffer_eps = sr.serial_connection(port=config.PORT_EPS,bauldrate=config.BAUDRATE)
    
    # Creating an iterable container to simplify going through all data
    buffers = [buffer_eps,buffer_ttic,buffer_obdh]

    for buffer in buffers:
        # Check for critical messages 
        code = log.log_handler(buffer)
        # Match for the type of the critical messages
        if code == log.CODE_TYPE.OK:
            continue
        elif code == log.CODE_TYPE.ERROR:
            log_date = time.strftime("[%d/%m/%Y] - %H:%M:%S")
            file_date = time.strftime("[%d/%m/%Y]")
            try:
                path = ("{}/log-{}.txt".format(config.PATH_FOR_LOGS,file_date))
                log_file = open(path,"a+")
                log_file.write("{} - CODE::ERROR -> {}".format(log_date,buffer))
                print("{} - CODE::ERROR -> {}".format(log_date,buffer))
                log_file.close()
            except:
                # TODO: Fix the generic exception 
                print("Error either on closing the file or creating a new one")
            # TODO Match of possible codes
        elif code == log.CODE_TYPE.RESET:
            log_date = time.strftime("[%d/%m/%Y] - %H:%M:%S")
            file_date = time.strftime("[%d/%m/%Y]")
            try:
                path = ("{}/log-{}.txt".format(config.PATH_FOR_LOGS,file_date))
                log_file = open(path,"a+")
                log_file.write("{} - CODE::RESET -> {}".format(log_date,buffer))
                print("{} - CODE::RESET -> {}".format(log_date,buffer))
                log_file.close()
            except:
                # TODO: Fix the generic exception 
                print("Error either on closing the file or creating a new one")
            # TODO Match of possible codes
            
