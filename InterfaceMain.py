import serial
import serial.tools.list_ports
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QMessageBox, QComboBox
)


def detect_bt_ports():
    """
    Return a list of all COM ports with their description.
    Example output:
    [('COM3', 'USB-SERIAL CH340'), ('COM4', 'Standard Serial over Bluetooth')]
    """
    ports = serial.tools.list_ports.comports()
    port_list = [(p.device, p.description) for p in ports]
    return port_list


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D4 Monocopter Bluetooth Controller")
        self.setWindowIcon(QIcon("Resources/logo_icon.jpg"))
        self.serial_conn = None

        # --- 1️⃣ Create central widget ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # --- 2️⃣ Layouts ---
        layout = QVBoxLayout()
        layout.setSpacing(15)
        central_widget.setLayout(layout)

        # --- Port selection ---
        self.port_label = QLabel("Select Bluetooth Port:")
        layout.addWidget(self.port_label)

        self.port_combo = QComboBox()
        self.refresh_ports()
        layout.addWidget(self.port_combo)

        refresh_btn = QPushButton("🔄 Refresh Ports")
        refresh_btn.clicked.connect(self.refresh_ports)
        layout.addWidget(refresh_btn)

        # --- Connect button ---
        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_serial)
        layout.addWidget(self.connect_btn)

        self.status_label = QLabel("Not connected")
        layout.addWidget(self.status_label)

        # --- Command input ---
        cmd_layout = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter command (e.g. A000, B000, C012)...")
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_command)
        cmd_layout.addWidget(self.cmd_input)
        cmd_layout.addWidget(send_btn)
        layout.addLayout(cmd_layout)

        # --- Quick command buttons ---
        quick_layout = QHBoxLayout()
        for cmd in ["A000", "B000", "C000"]:
            btn = QPushButton(cmd)
            btn.clicked.connect(lambda _, c=cmd: self.send_quick_command(c))
            quick_layout.addWidget(btn)
        layout.addLayout(quick_layout)

    def refresh_ports(self):
        ports = detect_bt_ports()  # returns list of tuples: (port, description)
        self.port_combo.clear()
        if ports:
            for port, desc in ports:
                # display description but store COM port as userData
                self.port_combo.addItem(f"{port} - {desc}", port)
            # select last port
            self.port_combo.setCurrentIndex(len(ports) - 1)
        else:
            self.port_combo.addItem("No COM ports found", None)

    def connect_serial(self):
        port = self.port_combo.currentData()  # retrieves only COM port (e.g., "COM11")
        if not port:
            QMessageBox.warning(self, "Error", "No valid port selected.")
            return
        try:
            self.serial_conn = serial.Serial(port, baudrate=9600, timeout=1)
            self.status_label.setText(f"✅ Connected on {port}")
            self.connect_btn.setEnabled(False)
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Failed to open {port}\n{e}")

    def send_command(self):
        if not self.serial_conn or not self.serial_conn.is_open:
            QMessageBox.warning(self, "Error", "Not connected to any port.")
            return
        cmd = self.cmd_input.text().strip()
        if cmd:
            self.serial_conn.write((cmd + "\r\n").encode())
            self.status_label.setText(f"Sent: {cmd}")
            self.cmd_input.clear()

    def send_quick_command(self, cmd):
        self.cmd_input.setText(cmd)
        self.send_command()


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
