# CommandWidget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox,QGroupBox, 
)

from PyQt6.QtCore import Qt

import struct


class PIDWidget(QGroupBox):
    def __init__(self, ble_manager, parent=None):
        super().__init__(parent, title="PID")

        self.ble_manager = ble_manager
        layout = QVBoxLayout()

        self.setLayout(layout)

        # --- P command input ---
        p_layout = QHBoxLayout()
        self.p_input = QLineEdit()
        self.p_input.setText("0.0")

        self.p_label = QLabel("P")
        self.p_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        p_layout.addWidget(self.p_label)
        p_layout.addWidget(self.p_input)
        layout.addLayout(p_layout)

        # --- I command input ---
        i_layout = QHBoxLayout()
        self.i_input = QLineEdit()
        self.i_input.setText("0.0")

        self.i_label = QLabel("I ")
        self.i_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        i_layout.addWidget(self.i_label)
        i_layout.addWidget(self.i_input)
        layout.addLayout(i_layout)

        # --- D command input ---
        d_layout = QHBoxLayout()
        self.d_input = QLineEdit()
        self.d_input.setText("0.0")

        self.d_label = QLabel("D")
        self.d_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        d_layout.addWidget(self.d_label)
        d_layout.addWidget(self.d_input)
        layout.addLayout(d_layout)

        # --- send command input ---
        button_layout = QHBoxLayout()
        self.send_btn = QPushButton("Send")
        self.toggle_pid_checkbox = QCheckBox("Toggle Regulation")

        button_layout.addWidget(self.send_btn)
        button_layout.addWidget(self.toggle_pid_checkbox)
        layout.addLayout(button_layout)

        self.send_btn.clicked.connect(self.send_PID_settings)

    def send_Toggle_PID(self):
        msg = struct.pack('=cI', b'G', int(self.toggle_pid_checkbox.isChecked()))
        print(msg)
        self.ble_manager.send_command(msg)
        
    def send_PID_settings(self):
        p = self.p_input.text().strip()
        i = self.i_input.text().strip()
        d = self.d_input.text().strip()

        p_val = self._validate_values(p)
        i_val = self._validate_values(i)
        d_val = self._validate_values(d)

        if p_val and i_val and d_val:
            self.status_label.setText("Ok")

            msg_p = struct.pack('=cf', b'P', float(p))
            msg_i = struct.pack('=cf', b'I', float(i))
            msg_d = struct.pack('=cf', b'D', float(d))

            self.ble_manager.send_command(msg_p)
            self.ble_manager.send_command(msg_i)
            self.ble_manager.send_command(msg_d)

    def _validate_values(self, value):
        try:
            value = float(value)
            return True
        except:
            self.status_label.setText("ERROR")
            return False

