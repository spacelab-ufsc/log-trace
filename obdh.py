# SCRIPT TO RUN

import time # Basically used to get local time
import config.config as cfg
import log_handlers.log_handler as log # Contains logic to detect important logs
import serial.read_serial as sr # Contains the logic to read from serial port

config:dict = cfg.load_config("OBDH")

while True:
    # Start reading Serial Port for all modules
    buffer = sr.serial_connection(port=config["path_sr_port"],baudrate=config["baudrate"])
    
    # Creating an iterable container to simplify going through all data

    # Check for critical messages 
    code = log.log_handler(buffer)
    # Match for the type of the critical messages
    # TODO Match of possible codes
    if code == log.CODE_TYPE.OK:
        continue
    elif code == log.CODE_TYPE.ERROR:
        log_date = time.strftime("[%d/%m/%Y] - %H:%M:%S")
        file_date = time.strftime("[%d/%m/%Y]")
        try:
            path = ("{}/log-{}.txt".format(config["path_file"],file_date))
            log_file = open(path,"a+")
            log_file.write("{} - CODE::ERROR -> {}".format(log_date,buffer))
            print("{} - CODE::ERROR -> {}".format(log_date,buffer))
            log_file.close()
        except (FileNotFoundError, PermissionError):
            print("Error either on closing the file or creating a new one")
        except (OSError, IOError):
            print("Error on writing to the file")
    elif code == log.CODE_TYPE.RESET:
        log_date = time.strftime("[%d/%m/%Y] - %H:%M:%S")
        file_date = time.strftime("[%d/%m/%Y]")
        try:
            path = ("{}/log-{}.txt".format(config["path_file"],file_date))
            log_file = open(path,"a+")
            log_file.write("{} - CODE::RESET -> {}".format(log_date,buffer))
            print("{} - CODE::RESET -> {}".format(log_date,buffer))
            log_file.close()
        except (FileNotFoundError, PermissionError):
            print("Error either on closing the file or creating a new one")
        except (OSError, IOError):
            print("Error on writing to the file")
        
