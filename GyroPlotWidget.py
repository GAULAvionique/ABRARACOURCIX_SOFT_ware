from PyQt6.QtWidgets import QWidget, QVBoxLayout
from collections import deque
import pyqtgraph as pg

class GyroPlotWidget(QWidget):
    def __init__(self, ble_manager, parent=None):
        super().__init__(parent)
        self.ble_manager = ble_manager

        # Connect BLEManager signal to plotting function
        self.ble_manager.new_line.connect(self.process_line)

        # Buffers
        self.max_points = 100
        self.timestamps = deque(maxlen=self.max_points)
        self.gyro_vals = deque(maxlen=self.max_points)

        # Layout and plot
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.plot_widget = pg.PlotWidget(title="Real-time Gyro")
        layout.addWidget(self.plot_widget)

        self.curve = self.plot_widget.plot(pen=pg.mkPen('y', width=2))

    def process_line(self, line):
        """
        Expects lines of the format: T_12345678;G_1.2345
        """
        if ';' not in line:
            return

        ts, gyro = None, None
        for part in line.split(';'):
            if part.startswith("T_"):
                try:
                    ts = float(part[2:])
                except ValueError:
                    return
            elif part.startswith("G_"):
                try:
                    gyro = float(part[2:])
                except ValueError:
                    return

        if ts is not None and gyro is not None:
            self.timestamps.append(ts)
            self.gyro_vals.append(gyro)
            self.curve.setData(list(self.timestamps), list(self.gyro_vals))
