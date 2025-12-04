# CommandWidget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QSpinBox,QGroupBox, 
)

from PyQt6.QtCore import Qt

import struct


class CurrentStateWidget(QGroupBox):
    
    def __init__(self, ble_manager, parent=None):
        super().__init__(parent, title="State")

        self.ble_manager = ble_manager
        self.last_state = self.ble_manager.last_state_value
        self.ble_manager.state_dict_update.connect(self.update)
        self.labels = []


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
            self.labels[i].setText(f"{key}: {self.last_state[key]}")


