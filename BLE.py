import time
import serial
import serial.tools.list_ports
from PyQt6.QtCore import QObject, pyqtSignal, QThread

BAUDRATE = 115200


class BLEWorker(QObject):
    new_line = pyqtSignal(str)

    def __init__(self, serial_conn):
        super().__init__()
        self.serial_conn = serial_conn
        self.running = True

    def start(self):
        while self.running:
            if self.serial_conn and self.serial_conn.is_open:
                line = self.serial_conn.readline().decode('utf-8').strip()
                if line:
                    self.new_line.emit(line)
            else:
                time.sleep(0.01)

    def stop(self):
        self.running = False

class BLEManager(QObject):
    new_line = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.serial_conn = None
        self.worker = None
        self.thread = None

    def connect(self, port=None):
        if port:
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
        self.worker.new_line.connect(self.new_line.emit)
        self.thread.start()

    def send_command(self, cmd):
        if self.serial_conn and self.serial_conn.is_open:
            self.serial_conn.write((cmd + "\r\n").encode())

    def stop(self):
            if self.worker:
                self.worker.stop()
            if self.thread:
                self.thread.quit()
                self.thread.wait()
            if self.serial_conn and self.serial_conn.is_open:
                self.serial_conn.close()

def detect_bt_ports():
    ports = serial.tools.list_ports.comports()
    return [(p.device, p.description) for p in ports]