import gi
gi.require_version("Gtk","3.0")

from gi.repository import Gtk

import serial
import serial.tools.list_ports as portlists
from serial.tools.miniterm import unichr
import re
import logging
import os
import threading
import time
from datetime import datetime


ERROR_CODE = "\033[1;31m"
BAUD = 115200
LOG_DIR = "/.Logs"

#here's for importing the other files of spacelab-transmitter that are missing or not ready

#CONSTANTS
_UI_FILE_LOCAL                  = os.path.abspath(os.path.dirname(__name__)) + '/data/ui/spacelab-Serial_COM.glade'
_UI_FILE_LINUX_SYSTEM           = '/usr/share/spacelab-Serial_COM/spacelab-Serial_COM.glade'

_CURRENT_DIR_LOCAL              = os.path.abspath(os.path.dirname(__name__))

_ICON_FILE_LOCAL                = os.path.abspath(os.path.dirname(__name__)) + '/data/img/spacelab_transmitter_256x256.png'

_LOGO_FILE_LOCAL                = os.path.abspath(os.path.dirname(__name__)) + '/data/img/spacelab-logo-full-400x200.png'

_DIR_CONFIG_LINUX               = '.spacelab-Serial_COM'

class Serial_COM:
    def __init__(self):
        self.builder = Gtk.Builder()
        
        # Importing .glade file
        if os.path.isfile(_UI_FILE_LOCAL):
            self.builder.add_from_file(_UI_FILE_LOCAL)
        else:
            self.builder.add_from_file(_UI_FILE_LINUX_SYSTEM)

        self.Serial_config = {
            "Serial_Port" : [None, "/dev/ttyUSB0", "/dev/ttyUSB1", "/dev/ttyUSB2", "/dev/ttyUSB3"],
            "Baud_Rate" : [1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200, 230400],
            "Parity" : [serial.PARITY_NONE, serial.PARITY_EVEN, serial.PARITY_ODD, serial.PARITY_MARK, serial.PARITY_SPACE],
            "Stop_bits" : [serial.STOPBITS_ONE , serial.STOPBITS_ONE_POINT_FIVE , serial.STOPBITS_TWO],
            "Data_bits" : [serial.FIVEBITS , serial.SIXBITS , serial.SEVENBITS , serial.EIGHTBITS]
        }

        self.Serial_Port = self.Serial_config["Serial_Port"][0]

        self.builder.connect_signals(self)
        self._build_widgets()
        self._load_preferences()

        self.run()

    def _build_widgets(self):

        # Main Window
        self.window = self.builder.get_object("CubeSAT_COM")
        if os.path.isfile(_ICON_FILE_LOCAL):
            self.window.set_icon_from_file(_ICON_FILE_LOCAL)
        else:
            pass
            # self.window.set_icon_from_file(_ICON_FILE_LINUX_SYSTEM)
        self.window.set_title("CubeSAT_COM")

        self.window.set_wmclass(self.window.get_title(), self.window.get_title())
        self.window.connect("destroy", self.onDestroy)

        # Action Buttons
        self.button_connect = self.builder.get_object("button_connect")
        self.button_connect.connect("clicked", self.serial_connection)

        self.button_disconnect = self.builder.get_object("button_disconnect")
        self.button_disconnect.connect("clicked", self.serial_disconnect)

        self.button_preferences = self.builder.get_object("button_preferences")
        self.button_preferences.connect("clicked", self.on_preferences_clicked)
        
        self.toolbutton_clean = self.builder.get_object("toolbutton_clean")
        self.toolbutton_clean.connect("clicked", self.on_toolbutton_clean_clicked)

        # Serial Commands
        self.Command = self.builder.get_object("Command")
        self.Command.connect("activate", self.on_Command_activate)

        self.Button_Send = self.builder.get_object("Button_Send")
        self.Button_Send.connect("clicked", self.on_Button_Send_clicked)

        self.Recieved_Text = self.builder.get_object("Received_Text")
        self.received_scroll = self.builder.get_object("received_scroll")

        self.Text_Commands = self.builder.get_object("Text_Commands")
        self.Commands_scroll = self.builder.get_object("Commands_scroll")

        # Serial Port Settings
        self.Serial_Port_Box1 = self.builder.get_object("Serial_Port1")
        self.Serial_Port_Box1.connect("changed", self.on_Serial_Port_Box1_changed)

        self.Baud_Rate_Box1 = self.builder.get_object("Baud_Rate1")
        self.Baud_Rate_Box1.connect("changed", self.on_Baud_Rate_Box1_changed)
        
        self.Send_option = self.builder.get_object("Send_Switch")

        # Log Settings
        self.Log_Dir = self.builder.get_object("Log_DIR")
        self.Module = self.builder.get_object("Module")
        self.Log_Record = self.builder.get_object("Record_Switch")

        self.Log_Dir.set_current_folder(_CURRENT_DIR_LOCAL + LOG_DIR)
        #self.Log_Dir.set_current_name(LOG_DIR)

        # Settings Window
        self.COMSettings = self.builder.get_object("COMSettings")
        self.COMSettings.set_title("COMSettings")

        # Settings Window Buttons
        self.Save_Preferences = self.builder.get_object("Save_Preferences")
        self.Save_Preferences.connect("clicked", self.on_Save_Preferences_clicked)

        self.Discard_Options = self.builder.get_object("Discard_Options")
        self.Discard_Options.connect("clicked", self.on_Discard_Options_clicked)

    def _load_preferences(self):
        self.button_connect.set_sensitive(True)
        self.button_disconnect.set_sensitive(False)
        self.button_preferences.set_sensitive(True)

        self.Command.set_editable(False)
        self.Command.set_sensitive(False)
        self.Button_Send.set_sensitive(False)
        self.Recieved_Text.set_editable(False)
        self.Recieved_Text.set_sensitive(False)
        self.Text_Commands.set_editable(False)
        self.Text_Commands.set_sensitive(False)

        # Serial Port Settings
        self.Serial_Port_Box = self.builder.get_object("Serial_Port")
        self.Baud_Rate_Box = self.builder.get_object("Baud_Rate")
        self.Parity_Box = self.builder.get_object("Parity")
        self.Stop_bits_Box = self.builder.get_object("Stop_bits")
        self.Data_bits_Box = self.builder.get_object("Data_bits")
        self.Flow_Control_Box = self.builder.get_object("Flow_Control")

        self.load_Settings()

        for comport in serial.tools.list_ports.comports(): self.Serial_Port_Box1.append_text(str(comport.device))
        self.Serial_Port_Box1.set_active_id(None)

        for baud in self.Serial_config["Baud_Rate"]: self.Baud_Rate_Box1.append_text(str(baud))
        self.Baud_Rate_Box1.set_active(next((index for index, row in enumerate(self.Baud_Rate_Box1.get_model()) if row[0] == str(115200)), -1))

    def remove_ansi_color(self, string: str) -> str:
        ansi_escape = re.compile(r"\x1b(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", string)

    def run(self):
        self.window.show_all()

        self.Serial = serial.Serial()
        self.thread = threading.Thread(target=self.Serial_Receive_event)   
        self.check_thread = threading.Thread(target=self.serial_check)

        self.check_thread.start()
        Gtk.main()

    def onDestroy(self, *args):
        self.update = False

        if self.thread.is_alive(): self.check_thread.join()
        if self.Serial.is_open: self.Serial.close()
        if self.thread.is_alive(): self.thread.join()

        Gtk.main_quit()    
   
    def serial_connection(self, widget):
        self.update = False
        self.check_thread.join()
    
        self.Serial_Settings_Load()

        self.Serial = serial.Serial(port=self.Serial_Port, baudrate=self.Baud_Rate, parity=self.Parity, stopbits=self.Stop_bits, bytesize=self.Data_bits, timeout=1)#, flowcontrol=self.Flow_Control)
        
        self.button_connect.set_sensitive(False)
        self.button_disconnect.set_sensitive(True)
        self.button_preferences.set_sensitive(False)

        self.Command.set_editable(True)
        self.Command.set_sensitive(True)
        self.Button_Send.set_sensitive(True)
        self.Recieved_Text.set_editable(False)
        self.Recieved_Text.set_sensitive(True)

        if self.Log_Record.get_active(): self.setup_logging(self.Module.get_active_text(), self.Log_Dir.get_current_folder())

        self.thread = threading.Thread(target=self.Serial_Receive_event) 
        self.thread.start()


    def serial_disconnect(self, widget):
        self.button_connect.set_sensitive(True)
        self.button_disconnect.set_sensitive(False)
        self.button_preferences.set_sensitive(True)

        self.Command.set_editable(False)
        self.Command.set_sensitive(False)
        self.Button_Send.set_sensitive(False)
        self.Recieved_Text.set_editable(False)
        self.Recieved_Text.set_sensitive(False)
        
        self.thread.join()
        self.Serial.close()
        
        self.check_thread = threading.Thread(target=self.serial_check)
        self.check_thread.start()        

    def on_preferences_clicked(self, button):
        self.PORT_update()
        self.COMSettings.show()

    def PORT_update(self):
        Serial_Ports = Gtk.ListStore(str)
        for comport in serial.tools.list_ports.comports(): Serial_Ports.append([str(comport.device)])

        self.Serial_Port_Box.set_model(Serial_Ports)
        self.Serial_Port_Box.set_active(next((index for index, row in enumerate(self.Serial_Port_Box.get_model()) if row[0] == str(self.Serial_Port)), -1))
        
        self.Serial_Port_Box1.set_model(Serial_Ports)
        self.Serial_Port_Box1.set_active(next((index for index, row in enumerate(self.Serial_Port_Box1.get_model()) if row[0] == str(self.Serial_Port)), -1))

    def serial_check(self):
        self.update = True
        while self.update:
            self.PORT_update()
            time.sleep(2)

    def load_Settings(self):
        for comport in serial.tools.list_ports.comports(): self.Serial_Port_Box.append_text(str(comport.device))
        self.Serial_Port_Box.set_active(next((index for index, row in enumerate(self.Serial_Port_Box.get_model()) if row[0] == "/dev/ttyUSB0"), -1))

        for baud in self.Serial_config["Baud_Rate"]: self.Baud_Rate_Box.append_text(str(baud))
        self.Baud_Rate_Box.set_active(next((index for index, row in enumerate(self.Baud_Rate_Box.get_model()) if row[0] == str(115200)), -1))

        for Parity in self.Serial_config["Parity"]:  self.Parity_Box.append_text(str(Parity))
        self.Parity_Box.set_active(next((index for index, row in enumerate(self.Parity_Box.get_model()) if row[0] == str(serial.PARITY_NONE)), -1))

        for stopbits in self.Serial_config["Stop_bits"]: self.Stop_bits_Box.append_text(str(stopbits))
        self.Stop_bits_Box.set_active(next((index for index, row in enumerate(self.Stop_bits_Box.get_model()) if row[0] == str(serial.STOPBITS_ONE)), -1))

        for databits in self.Serial_config["Data_bits"]: self.Data_bits_Box.append_text(str(databits))
        self.Data_bits_Box.set_active(next((index for index, row in enumerate(self.Data_bits_Box.get_model()) if row[0] == str(serial.EIGHTBITS)), -1))

    def on_Serial_Port_Box1_changed(self, widget):
        self.Serial_Port = widget.get_active_text()
        self.Serial_Port_Box.set_active(next((index for index, row in enumerate(self.Serial_Port_Box.get_model()) if row[0] == widget.get_active_text()), -1))

    def on_Baud_Rate_Box1_changed(self, widget):
        self.Baud_Rate = next((baud for baud in self.Serial_config["Baud_Rate"] if str(baud) == widget.get_active_text()), 115200)
        self.Baud_Rate_Box.set_active(next((index for index, row in enumerate(self.Baud_Rate_Box1.get_model()) if row[0] == str(widget.get_active_text())), -1))

    def Serial_Receive_event(self):
        while self.Serial.is_open and self.button_disconnect.get_sensitive():
            self.receive_command(self.Serial.readline().decode()) if self.Serial.in_waiting else None
            
    def on_Save_Preferences_clicked(self, button):
        self.Serial_Settings_Load()
        self.Serial_Port_Box1.set_active(next((index for index, row in enumerate(self.Serial_Port_Box1.get_model()) if row[0] == self.Serial_Port_Box.get_active_text()), -1))
        self.Baud_Rate_Box1.set_active(next((index for index, row in enumerate(self.Baud_Rate_Box1.get_model()) if row[0] == str(self.Baud_Rate_Box.get_active_text())), -1))
        self.COMSettings.hide()

    def Serial_Settings_Load(self):
        self.Serial_Port = self.Serial_Port_Box.get_active_text()
        self.Baud_Rate = next((baud for baud in self.Serial_config["Baud_Rate"] if str(baud) == self.Baud_Rate_Box.get_active_text()), 115200)
        self.Parity = next((parity for parity in self.Serial_config["Parity"] if str(parity) == self.Parity_Box.get_active_text()), serial.PARITY_NONE)
        self.Stop_bits = next((stopbits for stopbits in self.Serial_config["Stop_bits"] if str(stopbits) == self.Stop_bits_Box.get_active_text()), serial.STOPBITS_ONE)
        self.Data_bits = next((databits for databits in self.Serial_config["Data_bits"] if str(databits) == self.Data_bits_Box.get_active_text()), serial.EIGHTBITS)

    def on_Discard_Options_clicked(self, button):
        self.COMSettings.hide()

    def on_Command_activate(self, widget, event):
        self.send_command()

    def on_Button_Send_clicked(self, button):
        self.send_command()
        print("To do...")

    def on_toolbutton_clean_clicked(self, button):
        self.Recieved_Text.set_buffer(Gtk.TextBuffer())

    def send_command(self):
        self.Serial.write(self.Command.get_text().encode())
        self.Command.set_text(None)

    def receive_command(self, text: str):
        received_text = self.Recieved_Text.get_buffer()
        received_text.insert(received_text.get_end_iter(), text,-1)
        self.Recieved_Text.set_buffer(received_text)
        adjustment = self.received_scroll.get_vadjustment()
        adjustment.set_value( adjustment.get_upper() ) if adjustment.get_upper() > adjustment.get_page_size() else adjustment.set_value( adjustment.get_upper() - adjustment.get_page_size() )
        if self.Log_Record.get_active(): self.save_logs(text)

    def setup_logging(self,module: str, log_dir: str):
        filename = log_dir + "/" + module + " " + str(datetime.now()) +".log"

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            print(f"Creating log directory on: {log_dir}")

        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("")
            print(f"Creating log file on: {filename}")

        logging.basicConfig(
            filename=filename,
            level=logging.DEBUG,
            format="[%(asctime)s][%(levelname)s] > %(message)s",
        )

    def save_logs(self, line: str):
        """
        Saves logs by removing ANSI color codes from the input line and logs the line with an error level if it contains an error code, otherwise logs with an info level.
        Parameters:
            line (str): The input line to be logged.
        Returns:
            None
        """
        logline = self.remove_ansi_color(line)
        
        if ERROR_CODE in line: 
            logging.error(logline)
        else: 
            logging.info(logline)

def main():
    prog = Serial_COM()
    
if __name__ == "__main__":
    main()
