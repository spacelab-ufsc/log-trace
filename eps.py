# SCRIPT TO RUN

import time  # Basically used to get local time
import config.config as cfg
import log_handlers.log_handler as log  # Contains logic to detect important logs
import serial.read_serial as sr  # Contains the logic to read from serial port

module = "EPS"
config: dict = cfg.load_config(module)

while True:
    # Start reading Serial Port for all modules
    buffer = sr.serial_connection(
        port=config["path_sr_port"], baudrate=config["baudrate"]
    )

    # Creating an iterable container to simplify going through all data

    # Check for critical messages
    code = log.log_handler(buffer)
    # Match for the type of the critical messages
    if code == log.CODE_TYPE.OK:
        continue
    if code == log.CODE_TYPE.ERROR:
        log_date = time.strftime("[%d/%m/%Y] - %H:%M:%S")
        file_date = time.strftime("[%d/%m/%Y]")
        try:
            path = f"{config['path_file']}/{module}-{file_date}.txt"
            log_file = open(path, "a+", encoding="ascii")
            log_file.write(f"{log_date} - CODE::ERROR -> {buffer}")
            print(f"{log_date} on {module} - CODE::ERROR -> {buffer}")
            log_file.close()
        except (FileNotFoundError, PermissionError):
            print("Error either on closing the file or creating a new one")
        except (OSError, IOError):
            print("Error on writing to the file")
    if code == log.CODE_TYPE.RESET:
        log_date = time.strftime("[%d/%m/%Y] - %H:%M:%S")
        file_date = time.strftime("[%d/%m/%Y]")
        try:
            path = f"{config['path_file']}/{module}-{file_date}.txt"
            log_file = open(path, "a+", encoding="ascii")
            log_file.write(f"{log_date} - CODE::RESET -> {buffer}")
            print(f"{log_date} on {module} - CODE::RESET -> {buffer}")
            log_file.close()
        except (FileNotFoundError, PermissionError):
            print("Error either on closing the file or creating a new one")
        except (OSError, IOError):
            print("Error on writing to the file")
