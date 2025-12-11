from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSlider, QSpinBox,QGroupBox, QComboBox, QCheckBox
)

from PyQt6.QtCore import Qt, pyqtSignal


name_plot1 = "Plot 1"
name_plot2 = "Plot 2"

class SelectPlotWidget(QGroupBox):
    plot1_var = pyqtSignal(list)
    plot2_var = pyqtSignal(list)

    def __init__(self, ble_manager, parent=None):
        super().__init__(parent, title="Custom plots")

        self.plot1_names = []
        self.plot2_names = []
        self.cur_plot_names = self.plot1_names
        self.cur_signal = self.plot1_var
        self.ble_manager = ble_manager
        self.values_name = self.ble_manager.values_name

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- combo 1 ---
        plot1_layout = QHBoxLayout()

        self.flush_button = QPushButton("Reset")

        self.plot_combo = QComboBox()
        self.plot_combo.addItem(name_plot1)
        self.plot_combo.addItem(name_plot2)

        plot1_layout.addWidget(self.plot_combo)
        plot1_layout.addWidget(self.flush_button)


        plot_options_layout = QVBoxLayout()
        self.checkboxes = []
        for name in self.values_name:
            checkbox = QCheckBox(f'{name}', self)
            self.checkboxes.append(checkbox)
            plot_options_layout.addWidget(checkbox)
            checkbox.stateChanged.connect(self.text_changed1)

        layout.addLayout(plot1_layout)
        layout.addLayout(plot_options_layout)

        self.plot_combo.currentTextChanged.connect(self.plot_changed)
        self.flush_button.clicked.connect(self.reset_plots)


    def combo_update(self, plot):
        print(plot)

    def text_changed1(self, state):
        checkbox = self.sender()
        header = checkbox.text()
        if state == 2:
            self.cur_plot_names.append(header)
        else:
            self.cur_plot_names.remove(header)

        self.cur_signal.emit(self.cur_plot_names)

    def plot_changed(self, plot_name):
        if plot_name == name_plot1:
            self.cur_plot_names = self.plot1_names
            self.cur_signal = self.plot1_var
        elif plot_name == name_plot2:
            self.cur_plot_names = self.plot2_names
            self.cur_signal = self.plot2_var
        self.set_plot_checkboxes()
    
    def set_plot_checkboxes(self):
        for checkbox in self.checkboxes:
            checkbox.stateChanged.disconnect()
            if checkbox.text() in self.cur_plot_names:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)
            checkbox.stateChanged.connect(self.text_changed1)

    def text_changed2(self, header):
        self.plot2_var.emit(header)

    def reset_plots(self):
        self.ble_manager.reset_state()