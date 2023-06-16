# Contains the handling of different log messages -> Ex: Error messages, Restart messages , etc
# TODO Choose all conditions to look for

from enum import Enum

class CODE_TYPE(Enum):
    OK = "OK"
    ERROR = "ERROR"
    RESET = "RESET"

def log_handler(str_stream):
    ERROR_LOG_CONDITION = "\033[31;1;"
    # TODO RESET_LOG_CONDITION = "_" 
    if str_stream.__contains__(ERROR_LOG_CONDITION):
        return CODE_TYPE.ERROR
    # TODO elif str_stream.__contains__(RESET_LOG_CONDITION):
        return ("RESET",str_stream)
    else:
        return CODE_TYPE.OK

