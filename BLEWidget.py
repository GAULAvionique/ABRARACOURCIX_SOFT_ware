# BLEWidget.py
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QMessageBox
from BLE import BLEManager
import serial

class BLEQWidget(QWidget):
    def __init__(self, ble_manager: BLEManager, parent=None):
        super().__init__(parent)
        self.ble_manager = ble_manager

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.port_combo = QComboBox()
        layout.addWidget(self.port_combo)

        self.refresh_btn = QPushButton("Refresh Ports")
        self.refresh_btn.clicked.connect(self.refresh_ble_port_list)
        layout.addWidget(self.refresh_btn)

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(self.connect_to_ble)
        layout.addWidget(self.connect_btn)

        self.status_label = QLabel("Not connected")
        layout.addWidget(self.status_label)

        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter command...")
        layout.addWidget(self.cmd_input)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_ble_command)
        layout.addWidget(self.send_btn)

        self.refresh_ble_port_list()

    def refresh_ble_port_list(self):
        ports = [(p.device, p.description) for p in serial.tools.list_ports.comports()]
        self.port_combo.clear()
        for port, desc in ports:
            self.port_combo.addItem(f"{port} - {desc}", port)

    def connect_to_ble(self):
        port = self.port_combo.currentData()
        if not port:
            QMessageBox.warning(self, "Error", "No port selected")
            return
        self.ble_manager.connect(port)
        self.status_label.setText(f"✅ Connected on {port}")
        self.connect_btn.setEnabled(False)

    def send_ble_command(self):
        cmd = self.cmd_input.text().strip()
        if cmd:
            self.ble_manager.send_command(cmd)
            self.cmd_input.clear()
