# CommandWidget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QSpinBox
)
from PyQt6.QtCore import Qt

class CommandWidget(QWidget):
    def __init__(self, ble_manager, parent=None):
        super().__init__(parent)
        self.ble_manager = ble_manager

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Custom command input ---
        custom_layout = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter command (e.g. C012)")
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(self.send_custom_command)
        custom_layout.addWidget(self.cmd_input)
        custom_layout.addWidget(send_btn)
        layout.addLayout(custom_layout)

        # --- Quick command buttons ---
        quick_layout = QHBoxLayout()
        self.arm_btn = QPushButton("Arm Drone")
        self.arm_btn.clicked.connect(lambda: self.ble_manager.send_command("A000"))
        self.stop_btn = QPushButton("Stop Drone")
        self.stop_btn.clicked.connect(lambda: self.ble_manager.send_command("C000"))
        quick_layout.addWidget(self.arm_btn)
        quick_layout.addWidget(self.stop_btn)
        layout.addLayout(quick_layout)

        # --- Motor speed slider ---
        motor_layout = QVBoxLayout()
        motor_slider_layout = QHBoxLayout()
        self.motor_slider = QSlider(Qt.Orientation.Horizontal)
        self.motor_slider.setRange(0, 100)
        self.motor_slider.setValue(15)
        self.motor_slider.setSingleStep(1)
        self.motor_slider.setMinimumWidth(150)
        self.motor_spin = QSpinBox()
        self.motor_spin.setRange(0, 100)
        self.motor_spin.setValue(15)
        self.motor_spin.setSuffix("%")
        self.motor_label = QLabel("Motor:")
        set_motor_btn = QPushButton("Set Motor Speed")
        set_motor_btn.clicked.connect(self.set_motor_speed)
        motor_slider_layout.addWidget(self.motor_label)
        motor_slider_layout.addWidget(self.motor_spin)
        motor_slider_layout.addWidget(self.motor_slider)
        motor_layout.addLayout(motor_slider_layout)
        motor_layout.addWidget(set_motor_btn)
        layout.addLayout(motor_layout)

        self.motor_slider.valueChanged.connect(self.motor_spin.setValue)
        self.motor_spin.valueChanged.connect(self.motor_slider.setValue)

    def send_custom_command(self):
        cmd = self.cmd_input.text().strip()
        if cmd:
            self.ble_manager.send_command(cmd)

    def set_motor_speed(self):
        speed = self.motor_slider.value()
        cmd = f"B{speed:03d}"
        self.ble_manager.send_command(cmd)
