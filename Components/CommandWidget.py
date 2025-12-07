# CommandWidget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QSpinBox, QGroupBox
)
from PyQt6.QtCore import Qt
import struct


class CommandWidget(QGroupBox):
    def __init__(self, ble_manager, parent=None):
        super().__init__(parent, title="Command")
        self.ble_manager = ble_manager

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Custom command input ---
        custom_layout = QHBoxLayout()
        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Enter command (e.g. C012)")
        send_btn = QPushButton("Send")
        send_btn.clicked.connect(lambda: self.send_custom_command(None))
        custom_layout.addWidget(self.cmd_input)
        custom_layout.addWidget(send_btn)
        layout.addLayout(custom_layout)

        # --- Quick command buttons ---
        quick_layout = QHBoxLayout()
        self.arm_btn = QPushButton("Arm Drone")
        self.arm_btn.clicked.connect(lambda: self.send_custom_command("A000"))
        self.stop_btn = QPushButton("Stop Drone")
        self.stop_btn.clicked.connect(lambda: self.send_custom_command("B000"))
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
        set_motor_btn.clicked.connect(lambda: self.send_custom_command(f"C{self.motor_spin.value()}"))
        motor_slider_layout.addWidget(self.motor_label)
        motor_slider_layout.addWidget(self.motor_spin)
        motor_slider_layout.addWidget(self.motor_slider)
        motor_layout.addLayout(motor_slider_layout)
        motor_layout.addWidget(set_motor_btn)
        layout.addLayout(motor_layout)

        # --- Consigne Vitesse ---
        #speed_slider_layout = QHBoxLayout()
        #self.setpoint_spin = QSpinBox()
        #self.setpoint_spin.setRange(0, 360)
        #self.setpoint_spin.setValue(0)
        #speed_slider_layout.addWidget(self.setpoint_spin)
        #self.set_speed_consign_btn = QPushButton("Set setpoint")
        #self.set_speed_consign_btn.clicked.connect(lambda: self.send_custom_command(f"V{self.setpoint_spin.value()}"))
        #speed_slider_layout.addWidget(self.set_speed_consign_btn)
        #layout.addLayout(speed_slider_layout)

        self.motor_slider.valueChanged.connect(self.motor_spin.setValue)
        self.motor_spin.valueChanged.connect(self.motor_slider.setValue)


    def set_motor_speed(self):
        speed = self.motor_slider.value()
        cmd = f"C{speed:03d}"
        self.send_custom_command(cmd)



    def send_custom_command(self, cmd=None):
        print(cmd)
        if cmd is None:
            cmd = self.cmd_input.text().strip()
            print(cmd)

        if cmd:
            if len(cmd) < 2:
                return
            command_type = cmd[0]
            value_part = cmd[1:]
            match command_type:
                case 'A'|'B':  # Arm | Stop
                    msg = struct.pack('=c', bytes(command_type, encoding="UTF-8"))
                    self.ble_manager.send_command(msg)

                case 'C'|'Z'|'S': # Set motor speed | Choose filter | Window size
                    msg = struct.pack('=cI', bytes(command_type, encoding="UTF-8"), int(value_part))
                    self.ble_manager.send_command(msg)

                case 'P'|'I'|'D'|'E'|'V'|'F':  # Paramètres PID | Alpha
                    msg = struct.pack('=cf', bytes(command_type, encoding="UTF-8"), float(value_part))
                    print(msg)
                    self.ble_manager.send_command(msg)

