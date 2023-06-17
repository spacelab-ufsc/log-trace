# Contains the handling of different log messages -> Ex: Error messages, Restart messages , etc

from enum import Enum

# All possible CODE STATUS
class CODE_TYPE(Enum):
    OK = "OK"
    ERROR = "ERROR"
    RESET = "RESET"

# TODO Check if theres more conditions to look for
# Encapsulates all conditions that are sought-after
class CODE_CONDITION(Enum):
    ERROR = "\033[1;31m"
    RESET_1 = "Last reset cause: " 

# Simply checks if the conditions are on stream buffer
def log_handler(str_stream):
    if str_stream.__contains__(CODE_CONDITION.ERROR.value):
        return CODE_TYPE.ERROR
    elif str_stream.__contains__(CODE_CONDITION.RESET_1.value):
        return CODE_TYPE.RESET
    else:
        return CODE_TYPE.OK













