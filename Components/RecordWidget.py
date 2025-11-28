# CommandWidget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QSpinBox,QGroupBox, 
)

from PyQt6.QtCore import Qt


class RecordWidget(QGroupBox):
    def __init__(self, ble_manager, parent=None):
        super().__init__(parent, title="Record")

        self.ble_manager = ble_manager
        layout = QVBoxLayout()

        self.setLayout(layout)

        # --- P command input ---
        p_layout = QHBoxLayout()
        self.p_input = QLineEdit()
        self.p_input.setText("0.0")

        self.p_label = QLabel("P")
        self.p_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        p_layout.addWidget(self.p_label)
        p_layout.addWidget(self.p_input)
        layout.addLayout(p_layout)

        slider_layout = QHBoxLayout()
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setRange(0, 60)
        self.time_slider.setValue(20)
        self.time_slider.setSingleStep(1)
        self.time_slider.setMinimumWidth(60)
        slider_layout.addWidget(self.time_slider)
        layout.addLayout(slider_layout)


        # --- send command input ---
        button_layout = QHBoxLayout()
        self.send_btn = QPushButton("Send")
        self.status_label = QLabel("Status")

        button_layout.addWidget(self.send_btn)
        button_layout.addWidget(self.status_label)
        layout.addLayout(button_layout)

        #self.send_btn.clicked.connect(self.send_PID_settings)

    def start_recording(self):
        pass
