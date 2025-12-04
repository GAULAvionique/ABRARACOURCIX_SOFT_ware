from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QComboBox, QMessageBox, QGroupBox
from Components.BLE import BLEManager
import serial

class BLEQWidget(QGroupBox):
    def __init__(self, ble_manager: BLEManager, parent=None):
        super().__init__(parent, title="Bluetooth")
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

        self.disconnect_btn = QPushButton("Disconnect")
        self.disconnect_btn.clicked.connect(self.disconnect_to_ble)
        layout.addWidget(self.disconnect_btn)
        self.disconnect_btn.setEnabled(False)

        self.status_label = QLabel("Status: ❌ Not connected")
        layout.addWidget(self.status_label)

        self.refresh_ble_port_list()

    def refresh_ble_port_list(self):
        ports = [(p.device, p.description) for p in serial.tools.list_ports.comports()]
        self.port_combo.clear()
        for port, desc in ports:
            self.port_combo.addItem(f"{port} - {desc}", port)
        self.port_combo.setCurrentIndex(len(ports) - 1)


    def connect_to_ble(self):
        port = self.port_combo.currentData()
        if not port:
            QMessageBox.warning(self, "Error", "No port selected")
            return
        try:
            self.ble_manager.connect(port)
        except:
            QMessageBox.warning(self, "Error", "Selected port is invalid")
            return
        self.status_label.setText(f"Status: ✅ Connected on {port}")
        self.connect_btn.setEnabled(False)
        self.disconnect_btn.setEnabled(True)
    
    def disconnect_to_ble(self):
        self.ble_manager.stop()
        self.connect_btn.setEnabled(True)
        self.disconnect_btn.setEnabled(False)
        self.status_label.setText("Status: ❌ Not connected")