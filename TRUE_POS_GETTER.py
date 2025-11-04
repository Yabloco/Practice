from  Default_interfaces import Default_node_interface
import csv

class TRUE_POS_GETTER(Default_node_interface):
    def __init__(self, params=None):
        self.csv_path = params[0]
        self.relative_point = params[1]
        with open(self.csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([])

    def __call__(self, Simulation_loop_handler):
        pos = Simulation_loop_handler.Robot.Get_camera_real_cords(self.relative_point)

        Simulation_loop_handler.loop_memory_dict['current_position'] = pos

        with open(self.csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            pos.insert(0, round(Simulation_loop_handler.sim.getSimulationTime(), 2))
            writer.writerows([pos])