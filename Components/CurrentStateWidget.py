# CommandWidget.py
from collections import deque
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QSpinBox,QGroupBox, 
)

from PyQt6.QtCore import Qt

import struct

FILTER_LENGTH = 100

class CurrentStateWidget(QGroupBox):
    
    def __init__(self, ble_manager, parent=None):
        super().__init__(parent, title="State")

        self.ble_manager = ble_manager
        self.last_state = self.ble_manager.last_state_value
        self.ble_manager.state_dict_update.connect(self.update)
        self.labels = []

        self.current_values = deque(maxlen=FILTER_LENGTH)
        self.battery_values = deque(maxlen=FILTER_LENGTH)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- P command input ---
        labels_layout = QVBoxLayout()
        for key in self.last_state.keys():
            label = QLabel(f"{key}: {self.last_state[key]}")
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            labels_layout.addWidget(label)
            self.labels.append(label)
            
        layout.addLayout(labels_layout)

    def update(self, state_dict):
        self.last_state = state_dict
        for i, key in enumerate(self.last_state.keys()):
            if key is 'current':
                self.current_values.append(self.last_state[key])
                avg_current = sum(self.current_values)/len(self.current_values)
                self.labels[i].setText(f"{key}: {avg_current:.2f}")
            elif key is 'voltage':
                self.battery_values.append(self.last_state[key])
                avg_voltage = sum(self.battery_values)/len(self.battery_values)
                self.labels[i].setText(f"{key}: {avg_voltage:.2f}")
            else:
                self.labels[i].setText(f"{key}: {self.last_state[key]}")


