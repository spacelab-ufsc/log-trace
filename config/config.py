import json

def load_config(module:str) -> dict:
    with open("./config.json", "r") as config_file:
        config:dict = json.load(config_file)
    baudrate = config["baudrate"]
    path_file = config["modules"][module]["path_file"]
    path_srport = config["modules"][module]["path_sr_port"]
    return {"baudrate": baudrate, "path_sr_port": path_srport, "path_file": path_file}

