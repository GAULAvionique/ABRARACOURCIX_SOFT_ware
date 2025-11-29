from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout)
from PyQt6.QtCore import QTimer

from Components.BLE import BLEManager
from Components.BLEWidget import BLEQWidget
from Components.CommandWidget import CommandWidget
from Components.GyroPlotWidget import GyroPlotWidget
from Components.PIDWidget import PIDWidget
from Components.RecordWidget import RecordWidget
from Components.SetpointWidget import SetpointWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.serial_conn = None
        self.ble_manager = BLEManager()
        self.UI_init()




    def UI_init(self):
   
        self.setWindowTitle("D4 Monocopter Bluetooth Controller")
        self.setWindowIcon(QIcon("Resources/logo_icon.jpg"))
        

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout()
        central.setLayout(main_layout)

        
        # --- Top layout with BLEWidget (left) + CommandWidget (right) ---
        top_layout = QHBoxLayout()
        main_layout.addLayout(top_layout)

        self.ble_widget = BLEQWidget(self.ble_manager)
        self.command_widget = CommandWidget(self.ble_manager)
        self.PID_widget = PIDWidget(self.ble_manager)
        self.Record_widget = RecordWidget(self.ble_manager)
        self.Setpoint_widget = SetpointWidget(self.ble_manager)


        top_layout.addWidget(self.ble_widget)
        top_layout.addWidget(self.command_widget)
        top_layout.addWidget(self.PID_widget)
        top_layout.addWidget(self.Record_widget)
        top_layout.addWidget(self.Setpoint_widget)


        # --- Bottom Graph ---
        self.gyro_plot = GyroPlotWidget(self.ble_manager)
        main_layout.addWidget(self.gyro_plot)

        
    def closeEvent(self, event):
        self.ble_manager.stop()
        event.accept()
