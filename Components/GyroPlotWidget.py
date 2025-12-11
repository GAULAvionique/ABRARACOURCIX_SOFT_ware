from PyQt6.QtWidgets import QWidget, QVBoxLayout
from collections import deque
import pyqtgraph as pg

from Components.CurrentStateWidget import FILTER_LENGTH

MAX_GRAPH_POINTS = 100
MIN_HEIGHT = 50
MAX_HEIGHT = 400
COLORS = ["r","g","b","c","m","y","k","w"]

class GyroPlotWidget(QWidget):
    def __init__(self, ble_manager, select_plot, parent=None):
        super().__init__(parent)
        self.time_val = 'time'
        self.plotted_val1 = []
        self.plotted_val2 = []

        self.curves_plot1 = {}
        self.curves_plot2 = {}

        self.current_values = deque(maxlen=FILTER_LENGTH)
        self.battery_values = deque(maxlen=FILTER_LENGTH)

        self.ble_manager = ble_manager
        self.select_plot = select_plot
        self.values_name = ble_manager.values_name

        self.ble_manager.new_dict.connect(self.process_data)
        self.select_plot.plot1_var.connect(self.update1)
        self.select_plot.plot2_var.connect(self.update2)

        self.values_deque_map = {self.values_name[i]:deque(maxlen=MAX_GRAPH_POINTS) for i in range(len(self.values_name))}

        layout = QVBoxLayout()
        self.setLayout(layout)

        # --- Raw gyro plot ---
        self.plot1 = pg.PlotWidget(title="Plot 1")
        self.plot1.setMinimumHeight(MIN_HEIGHT)
        self.plot1.setMaximumHeight(MAX_HEIGHT)
        self.plot1.addLegend()
        layout.addWidget(self.plot1)

        # --- Raw gyro plot ---
        self.plot2 = pg.PlotWidget(title="Plot 2")
        self.plot2.setMinimumHeight(MIN_HEIGHT)
        self.plot2.setMaximumHeight(MAX_HEIGHT)
        self.plot2.addLegend()
        layout.addWidget(self.plot2)

    # process newly received data
    def process_data(self, data):
        if self.ble_manager.flush_flag:
            self.flush_data()
            
        header = list(data.keys())[0]
        data = data[header]
        if header == 'current':
            self.current_values.append(data)
            avg_current = sum(self.current_values)/len(self.current_values)
            self.values_deque_map[header].append(avg_current)
        elif header == 'voltage':
            self.battery_values.append(data)
            avg_voltage = sum(self.battery_values)/len(self.battery_values)
            self.values_deque_map[header].append(avg_voltage)
        else:
            self.values_deque_map[header].append(data)
        
        # new points ready to be plotted
        if header == 'time':
            self.set_graphs(self.curves_plot1)
            self.set_graphs(self.curves_plot2)

    # updates all of a graph's curves
    def set_graphs(self, curves_plot):
        for header in curves_plot.keys():
            self.set_graph(curves_plot[header], self.time_val, header)

    # updates a single variable's plot
    def set_graph(self, curve, var_x, var_y):
        x_points = list(self.values_deque_map[var_x])
        y_points = list(self.values_deque_map[var_y])

        max_length = min(len(x_points), len(y_points))

        curve.setData(x_points[:max_length], y_points[:max_length])

    # Updates the displayed curves. headers contains the list of variables to display
    def update1(self, headers):
        print(headers)
        self.plotted_val1 = headers
        self._remove_curves(self.plot1, self.curves_plot1)
        self.curves_plot1 = {}
        self._update_plot_curves(self.plot1, self.plotted_val1, self.curves_plot1)

    def update2(self, headers):
        print(headers)
        self.plotted_val2 = headers
        self._remove_curves(self.plot2, self.curves_plot2)
        self.curves_plot2 = {}
        self._update_plot_curves(self.plot2, self.plotted_val2, self.curves_plot2)

    # util function to remove all currently displayed variables plot
    def _remove_curves(self, plot, curves_plot):
        for curve in curves_plot.keys():
            plot.removeItem(curves_plot[curve])

    # util function to create all desired variables plot
    def _update_plot_curves(self, plot, headers, curves_plot):
        for i, header in enumerate(headers):
            curves_plot[header] = plot.plot(pen=pg.mkPen(COLORS[i%len(COLORS)], width=2), name=header)

    def flush_data(self):
        for header in self.values_deque_map.keys():
            self.values_deque_map[header] = []
        self.ble_manager.flush_flag = False