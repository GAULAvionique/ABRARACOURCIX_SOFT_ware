from PyQt6.QtWidgets import QWidget, QVBoxLayout
from collections import deque
import pyqtgraph as pg

MAX_GRAPH_POINTS = 100
FILTER_COEFF = 0.5
FILTER_LENGTH = 50

class GyroPlotWidget(QWidget):
    def __init__(self, ble_manager, parent=None):
        super().__init__(parent)
        self.ble_manager = ble_manager

        self.ble_manager.new_line.connect(self.process_line)


        self.timestamps = deque(maxlen=MAX_GRAPH_POINTS)
        self.avg_gyro_vals = deque(maxlen=MAX_GRAPH_POINTS)
        self.raw_gyro_vals = deque(maxlen=MAX_GRAPH_POINTS)
        self.filter_values = deque([0.0]*FILTER_LENGTH, maxlen=FILTER_LENGTH)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Filtered gyro plot ---
        self.filtered_plot = pg.PlotWidget(title="Filtered Gyro")
        self.filtered_plot.setMinimumHeight(300)
        self.filtered_curve = self.filtered_plot.plot(pen=pg.mkPen('y', width=2))
        layout.addWidget(self.filtered_plot)

        # --- Raw gyro plot ---
        self.raw_plot = pg.PlotWidget(title="Raw Gyro")
        self.raw_plot.setMinimumHeight(300)
        self.raw_curve = self.raw_plot.plot(pen=pg.mkPen('r', width=2))
        layout.addWidget(self.raw_plot)

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
            
            # Raw values
            self.raw_gyro_vals.append(gyro)
            self.timestamps.append(ts)
            self.raw_curve.setData(list(self.timestamps), list(self.raw_gyro_vals))

            # On shift les valeurs
            self.filter_values.append(gyro)
            avg = 0.0
            coeff = FILTER_COEFF

            # On calul le filtre (avg)
            for val in reversed(self.filter_values):
                avg += coeff * val
                coeff /= 2.0

            self.avg_gyro_vals.append(avg)
            self.filtered_curve.setData(list(self.timestamps), list(self.avg_gyro_vals))
