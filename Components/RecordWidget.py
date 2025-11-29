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

        # --- duration command input ---
        duration_layout = QHBoxLayout()
        self.p_label = QLabel(f"Duration: ")
        self.p_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(0, 60)
        self.duration_spin.setValue(0)
        self.duration_spin.setSuffix('s')

        duration_layout.addWidget(self.p_label)
        duration_layout.addWidget(self.duration_spin)

        # --- slider ---
        slider_layout = QHBoxLayout()
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setRange(0, 60)
        self.time_slider.setValue(0)
        self.time_slider.setSingleStep(1)
        self.time_slider.setMinimumWidth(60)

        slider_layout.addWidget(self.time_slider)

        layout.addLayout(duration_layout)
        layout.addLayout(slider_layout)

        self.time_slider.valueChanged.connect(self.duration_spin.setValue)
        self.duration_spin.valueChanged.connect(self.time_slider.setValue)


        # --- send command input ---
        button_layout = QHBoxLayout()
        self.send_btn = QPushButton("Record")

        button_layout.addWidget(self.send_btn)
        layout.addLayout(button_layout)

        self.send_btn.clicked.connect(self.start_recording)

    def start_recording(self):
        self.ble_manager.record_data(self.duration_spin.value())

    def update_duration_label(self):
        self.p_label.setText(f"Duration:")
