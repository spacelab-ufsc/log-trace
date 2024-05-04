import serial
import argparse
import re
import logging
import os

ERROR_CODE = "\033[1;31m"
BAUD = 115200
LOG_DIR = "logs"

def remove_ansi_color(string: str) -> str:
    ansi_escape = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", string)

def setup_logging(module: str, log_dir: str):
    filename = "./" + log_dir + "/" + module + ".log"

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Creating log directory on: ./{log_dir}")

    if not os.path.exists(filename):
        with open(filename, "w") as f:
            f.write("")
        print(f"Creating log file on: {filename}")

    logging.basicConfig(
        filename=filename,
        level=logging.DEBUG,
        format="[%(asctime)s][%(levelname)s] > %(message)s",
    )

def save_logs(line: str):
    logline = remove_ansi_color(line)

    if ERROR_CODE in line:
        logging.error(logline)
    else:
        logging.info(logline)

def serial_connection(port, baudrate):
    stream = serial.Serial(port=port, baudrate=baudrate)
    return stream

def serial_read(stream: serial.Serial) -> str:
    b_buffer = stream.readline()
    return b_buffer.decode("iso-8859-1", "ignore")

def log_trace_cli():
    cli_parser = argparse.ArgumentParser(
        prog="log_trace.py",
        description="Reads the floripasat-2 modules log through UART",
    )

    cli_parser.add_argument("PORT", type=str, help="serial port to listen to")

    cli_parser.add_argument(
        "-f",
        "--log_file",
        action="store",
        default="module",
        type=str,
        help="sets the log file name",
    )

    cli_parser.add_argument(
        "-d",
        "--log_dir",
        action="store",
        default=LOG_DIR,
        type=str,
        help="sets the log directory",
    )

    args = cli_parser.parse_args()

    setup_logging(args.log_file, args.log_dir)

    dev = serial_connection(args.PORT, BAUD)

    try:
        while True:
            log_line = serial_read(dev)
            print(log_line, end="")
            save_logs(log_line)

    except KeyboardInterrupt:
        print("Keyboard interrupt detected. Exiting...")

    finally:
        dev.close()

if __name__ == "__main__":
    log_trace_cli()
