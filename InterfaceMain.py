from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout)

from BLE import BLEManager
from BLEWidget import BLEQWidget
from GyroPlotWidget import GyroPlotWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("D4 Monocopter Bluetooth Controller")
        self.setWindowIcon(QIcon("Resources/logo_icon.jpg"))
        self.serial_conn = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.ble_manager = BLEManager()

        self.ble_widget = BLEQWidget(self.ble_manager)
        layout.addWidget(self.ble_widget)

        self.gyro_plot = GyroPlotWidget(self.ble_manager)
        layout.addWidget(self.gyro_plot)

    def closeEvent(self, event):
        self.ble_manager.stop()
        event.accept()
