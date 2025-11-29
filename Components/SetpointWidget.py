# CommandWidget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QSpinBox, QGroupBox, QCheckBox
)
from PyQt6.QtCore import Qt, QTimer
import struct


class SetpointWidget(QGroupBox):
    def __init__(self, ble_manager, parent=None):
        super().__init__(parent, title="Setpoint")
        self.init_UI()
        self.ble_manager = ble_manager
        self.speed_count = 0

        self.timer = QTimer(self)
        # self.timer.singleShot(2000,self.update_function)  # for one time call only
        self.timer.timeout.connect(self.set_pursuit_speed)


        
    def pursuit_check(self):
        self.setpoint_spin2.setVisible(self.checkbox.isChecked())
        self.speed2_label.setVisible(self.checkbox.isChecked())
        self.duration_label.setVisible(self.checkbox.isChecked())
        self.time_slider.setVisible(self.checkbox.isChecked())
        self.duration_spin.setVisible(self.checkbox.isChecked())

    def send_custom_command(self, cmd=None):
        self.speed1 = self.setpoint_spin.value()
        self.speed2 = self.setpoint_spin2.value()
        self.duration = self.duration_spin.value()
        self.pursuit_mode = self.checkbox.isChecked()

        print(f"speed1: {self.speed1}")
        print(f"speed2: {self.speed2}")
        print(f"duration: {self.duration}")
        print(f"pursuit mode: {self.pursuit_mode}")

        if self.pursuit_mode:
            self.speed_count = 0
            self.timer.start(self.duration * 1000)
        else:
            self.timer.stop()
            self.send_setpoint(self.speed1)

    def set_pursuit_speed(self):        
        speed2send = self.speed1 if self.speed_count % 2 == 0 else self.speed2
        self.speed_count += 1
        self.send_setpoint(speed2send)

    def send_setpoint(self, speed):
        print(f"speed: {speed}")
        msg = struct.pack('=cf', bytes('V', encoding="UTF-8"), float(speed))
        self.ble_manager.send_command(msg)

    def init_UI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        # --- pursuit setpoint ---
        checkbox_layout = QHBoxLayout()
        self.checkbox = QCheckBox("pursuit")
        checkbox_layout.addWidget(self.checkbox)
        layout.addLayout(checkbox_layout)
        
        self.checkbox.stateChanged.connect(self.pursuit_check)

        # --- Consigne Vitesse 1 ---
        speed_slider_layout = QHBoxLayout()
        self.speed1_label = QLabel("speed 1:")
        self.speed1_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setpoint_spin = QSpinBox()
        self.setpoint_spin.setRange(0, 360)
        self.setpoint_spin.setValue(0)
        speed_slider_layout.addWidget(self.speed1_label)
        speed_slider_layout.addWidget(self.setpoint_spin)
        layout.addLayout(speed_slider_layout)

        # --- Consigne Vitesse 2 ---
        self.speed_slider_layout2 = QHBoxLayout()
        self.speed2_label = QLabel("speed 2:")
        self.speed2_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.setpoint_spin2 = QSpinBox()
        self.setpoint_spin2.setRange(0, 360)
        self.setpoint_spin2.setValue(0)
        self.speed_slider_layout2.addWidget(self.speed2_label)
        self.speed_slider_layout2.addWidget(self.setpoint_spin2)
        layout.addLayout(self.speed_slider_layout2)

        # --- Duration pulse setpoint ---
        duration_layout = QHBoxLayout()
        self.duration_label = QLabel(f"Duration: ")
        self.duration_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(4, 10)
        self.duration_spin.setValue(4)
        self.duration_spin.setSuffix('s')

        duration_layout.addWidget(self.duration_label)
        duration_layout.addWidget(self.duration_spin)

        # --- slider ---
        slider_layout = QHBoxLayout()
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setRange(4, 10)
        self.time_slider.setValue(4)
        self.time_slider.setSingleStep(1)
        self.time_slider.setMinimumWidth(60)

        slider_layout.addWidget(self.time_slider)

        layout.addLayout(duration_layout)
        layout.addLayout(slider_layout)

        self.time_slider.valueChanged.connect(self.duration_spin.setValue)
        self.duration_spin.valueChanged.connect(self.time_slider.setValue)

        self.time_slider.valueChanged.connect(self.duration_spin.setValue)
        self.duration_spin.valueChanged.connect(self.time_slider.setValue)
        
        self.pursuit_check()

        # --- send setpoint.s ---
        layout_send_btn = QHBoxLayout()
        self.set_speed_consign_btn = QPushButton("Set setpoint")
        self.set_speed_consign_btn.clicked.connect(self.send_custom_command)
        layout_send_btn.addWidget(self.set_speed_consign_btn)
        layout.addLayout(layout_send_btn)