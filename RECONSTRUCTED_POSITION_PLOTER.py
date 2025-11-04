from  Default_interfaces import Default_node_interface
import matplotlib.pyplot as plt
import pandas as pd

class RECONSTRUCTED_POSITION_PLOTER(Default_node_interface):

    def __init__(self, params=None):
        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_title("Траектория востановленная")
        self.fig.canvas.manager.window.wm_geometry("+150+100")
    def __call__(self, Simulation_loop_handler):
        try:
            data = pd.read_csv('Reconstructed_path.csv')
        except pd.errors.EmptyDataError:
            return

        x_col = data.columns[1]
        y_col = data.columns[3]
        self.ax.scatter(data[x_col], data[y_col])
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        self.ax.clear()