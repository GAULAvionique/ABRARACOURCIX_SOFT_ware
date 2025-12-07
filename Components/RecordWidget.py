# CommandWidget.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QSpinBox,QGroupBox, QFileDialog
)

from PyQt6.QtCore import Qt

MIN_RECORD_TIME = 1
MAX_RECORD_TIME = 30

recording_msg = "🟢 recording"
not_recording_msg = "🔴 not recording"


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
        self.duration_spin.setRange(MIN_RECORD_TIME, MAX_RECORD_TIME)
        self.duration_spin.setValue(MIN_RECORD_TIME)
        self.duration_spin.setSuffix('s')

        duration_layout.addWidget(self.p_label)
        duration_layout.addWidget(self.duration_spin)

        # --- slider ---
        slider_layout = QHBoxLayout()
        self.time_slider = QSlider(Qt.Orientation.Horizontal)
        self.time_slider.setRange(MIN_RECORD_TIME, MAX_RECORD_TIME)
        self.time_slider.setValue(MIN_RECORD_TIME)
        self.time_slider.setSingleStep(1)
        self.time_slider.setMinimumWidth(MAX_RECORD_TIME)

        slider_layout.addWidget(self.time_slider)

        layout.addLayout(duration_layout)
        layout.addLayout(slider_layout)

        self.time_slider.valueChanged.connect(self.duration_spin.setValue)
        self.duration_spin.valueChanged.connect(self.time_slider.setValue)

        # --- file name ---
        file_layout = QHBoxLayout()
        self.file_input = QLineEdit()
        self.file_input.setText("data.csv")
        self.file_label = QLabel("File name")
        self.file_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        file_layout.addWidget(self.file_label)
        file_layout.addWidget(self.file_input)
        layout.addLayout(file_layout)


        # --- file path selection ---
        path_layout = QHBoxLayout()
        self.file_explorer_btn = QPushButton("Open explorer")
        self.file_explorer_btn.clicked.connect(self.openFileDialog) 
        path_layout.addWidget(self.file_explorer_btn)
        layout.addLayout(path_layout)
        

        # --- send command input ---
        button_layout = QHBoxLayout()
        self.send_btn = QPushButton("Record")
        self.recording_label = QLabel(not_recording_msg)
        self.recording_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.addWidget(self.send_btn)
        button_layout.addWidget(self.recording_label)
        layout.addLayout(button_layout)

        self.send_btn.clicked.connect(self.start_recording)
        self.ble_manager.recording_ended.connect(self.recording_stopped)

    def start_recording(self):
        self.recording_label.setText(recording_msg)
        self.ble_manager.file_name = self.file_input.text().strip()
        self.ble_manager.start_record(self.duration_spin.value())

    def update_duration_label(self):
        self.p_label.setText(f"Duration:")

    def openFileDialog(self):
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Open File")
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if file_dialog.exec():
            selected_files = file_dialog.selectedFiles()
            self.ble_manager.file_path = selected_files[0] + "/"
            print("Selected File:", selected_files[0])

    def recording_stopped(self, value):
        self.recording_label.setText(not_recording_msg)