import time
import serial
import serial.tools.list_ports
from PyQt6.QtCore import QObject, pyqtSignal, QThread, QTimer

import pandas as pd

def to_float(data):
    return float(data)

def to_int(data):
    return int(data)

BAUDRATE = 115200

stop_recording = False
values_name = ["Speed",
               "Commande",
               "Error",
               "IntErr",
               "kp",
               "ki",
               "kd",
               "time",
               "filter_type",
               "current",
               "voltage",
               "Servo"]

headers = ["S","C","E","N","P","I","D","T","F","A","B","L"]

headers_type_func = [to_float,
                        to_float,
                        to_float,
                        to_float,
                        to_float,
                        to_float,
                        to_float,
                        to_int,
                        to_int,
                        to_float,
                        to_float,
                        to_float]

headers_to_dict_map = {headers[i]:values_name[i] for i in range(len(headers))}

headers_to_type_func_map = {headers[i]:headers_type_func[i] for i in range(len(headers))}



class BLEWorker(QObject):
    new_line = pyqtSignal(str)

    def __init__(self, serial_conn):
        super().__init__()
        self.serial_conn = serial_conn
        self.running = True

    def start(self):
        time_Start = time.time()

        while self.running:
            if self.serial_conn and self.serial_conn.is_open:
                
                line = self.serial_conn.readline().decode('utf-8').strip()

                if line:
                    self.new_line.emit(line)
                    
            else:
                time.sleep(0.001)

    def stop(self):
        self.running = False


class BLEManager(QObject):
    new_line = pyqtSignal(str)
    new_dict = pyqtSignal(dict)
    state_dict_update = pyqtSignal(dict)
    recording_ended = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.serial_conn = None
        self.worker = None
        self.thread = None
        
        self.values = self.init_values_dict()
        self.last_state_value = self.init_last_state_dict()
        self.headers = headers
        self.values_name = values_name

        self.record_timer = QTimer(self)
        self.record_timer.timeout.connect(self.stop_record)
        self.recording = False
        self.file_name = "data.csv"
        self.file_path = "./"

    def connect(self, port=None):
        if port:
            #port = 'COM5'
            self.serial_conn = serial.Serial(port, BAUDRATE, timeout=1)
            self.start_worker()

    def start_worker(self):
        if self.serial_conn is None:
            raise RuntimeError("Serial connection not established")

        # Avoid starting multiple threads
        if self.thread and self.thread.isRunning():
            return

        self.worker = BLEWorker(self.serial_conn)
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.start)
        self.worker.new_line.connect(self.update)
        #self.worker.new_line.connect(self.new_line.emit)
        self.thread.start()

    def send_command(self, cmd):
        if self.serial_conn and self.serial_conn.is_open:
            print(len(cmd))
            print(cmd)
            self.serial_conn.write(cmd + b'\n')

    def stop(self):
            if self.worker:
                self.worker.stop()
            if self.thread:
                self.thread.quit()
                self.thread.wait()
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()

    def init_values_dict(self):
        return {name:[] for name in values_name}

    def init_last_state_dict(self):
        return {name:0 for name in values_name}

    def update(self, package):
        self._process_data(package)

    def _process_data(self, package):
        try:
            header, data = self._parse_package(package)
        except:
            print("Error while decoding ignoring package")
            return
        
        #if record
        try:
            data = headers_to_type_func_map[header](data)
        except:
            print("Could not convert data to float or int")
            return
        # append la nouvelle valeur à la bonne liste dans le dict

        if self.recording:
            self.values[headers_to_dict_map[header]].append(data)

        # sends data to plot widgets.
        self.last_state_value[headers_to_dict_map[header]] = data

        self.new_dict.emit({headers_to_dict_map[header]:data})
        self.state_dict_update.emit(self.last_state_value)


    def _parse_package(self, package):
        
        try:
            split_package = package.split(';')
        except:
            raise("error parsing the data. no ';'")
        if len(split_package) != 2:
            raise("error parsing the data. wrong formating: {package}")

        package, new_line = split_package[0], split_package[1]
        header = package[0]
        data = package[1:]

        return header, data

    def start_record(self, duration):
        self.values = self.init_values_dict()
        self.recording = True
        self.record_timer.start(duration * 1000)
        print('recording')

    def stop_record(self):
        print('recording ended')
        self.record_timer.stop()
        self.recording = False
        save_to_csv(self.values, self.file_path + self.file_name)
        self.values = self.init_values_dict()
        self.recording_ended.emit(1)


def detect_bt_ports():
    ports = serial.tools.list_ports.comports()
    return [(p.device, p.description) for p in ports]


def save_to_csv(data, path):
    data = trim_data(data)
    try:
        df = pd.DataFrame.from_dict(data)
    except:
        print(f"An error occured while saving the data...")
    try:
        df.to_csv(path, index=False)
    except:
        print(f"Couldn't save to csv. Invalid path: {path}")

def trim_data(data):
    lengths = []
    for key in data.keys():
        lengths.append(len(data[key]))

    min_len = min(lengths)

    for key in data.keys():
        data[key] = data[key][:min_len]

    return data
