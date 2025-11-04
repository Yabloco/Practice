from  Default_interfaces import Default_node_interface
import numpy as np
import csv
from scipy.spatial.transform import Rotation
from copy import deepcopy

class TRAJECTORY_RECONSTRUCTOR(Default_node_interface):
    def __init__(self, params=None):
        self.csv_path = params[0]
        with open(self.csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([])

    def __call__(self, Simulation_loop_handler):
        Simulation_loop_handler.loop_memory_dict['Unprocessed_cords_from_TR'] = False

        if Simulation_loop_handler.loop_memory_dict.get('last_calculated_relative_motion') is None:
            return None
        if Simulation_loop_handler.loop_memory_dict.get('current_reconstructed_position') is None:
            Simulation_loop_handler.loop_memory_dict['current_reconstructed_position'] = np.array([0, 0, 0, 0, 0, 0])

        R, T = Simulation_loop_handler.loop_memory_dict.get('last_calculated_relative_motion')
        global_position = Simulation_loop_handler.loop_memory_dict.get('current_reconstructed_position')[:3]
        global_orientation = Rotation.from_rotvec(
            Simulation_loop_handler.loop_memory_dict.get('current_reconstructed_position')[3:]
        )

        delta_rotation = Rotation.from_matrix(R)
        new_global_orientation = Rotation.as_rotvec(delta_rotation * global_orientation)

        relative_delta_motion = -np.array(T).flatten()
        # Переводим вектор движения в глобальную СК через ТЕКУЩУЮ ориентацию
        global_delta_motion = global_orientation.apply(relative_delta_motion)
        new_global_position = global_position + global_delta_motion
        new_position_concat = list(
            np.concatenate(
                (new_global_position, new_global_orientation),
                axis=0
            )
        )
        Simulation_loop_handler.loop_memory_dict['current_reconstructed_position'] = new_position_concat
        with open(self.csv_path, 'a', newline='') as file:
            writer = csv.writer(file)
            pos = deepcopy(new_position_concat)
            pos.insert(0, round(Simulation_loop_handler.sim.getSimulationTime(), 2))
            writer.writerows([pos])
            Simulation_loop_handler.loop_memory_dict['Unprocessed_cords_from_TR'] = True