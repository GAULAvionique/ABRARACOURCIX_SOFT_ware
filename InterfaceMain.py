from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout)

from BLE import BLEManager
from BLEWidget import BLEQWidget
from CommandWidget import CommandWidget
from GyroPlotWidget import GyroPlotWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D4 Monocopter Bluetooth Controller")
        self.setWindowIcon(QIcon("Resources/logo_icon.jpg"))
        self.serial_conn = None

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        self.ble_manager = BLEManager()

        # --- Top layout with BLEWidget (left) + CommandWidget (right) ---
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        self.ble_widget = BLEQWidget(self.ble_manager)
        self.command_widget = CommandWidget(self.ble_manager)

        top_layout.addWidget(self.ble_widget)
        top_layout.addWidget(self.command_widget)

        # --- Bottom Graph ---
        self.gyro_plot = GyroPlotWidget(self.ble_manager)
        main_layout.addWidget(self.gyro_plot)
    def closeEvent(self, event):
        self.ble_manager.stop()
        event.accept()
