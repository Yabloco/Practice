from  Default_interfaces import Default_node_interface
import cv2
import os

class IMAGE_LOADER(Default_node_interface):
    def __init__(self, params=None):

        self.load_dir = params[0]
        if self.load_dir:
            for filename in os.listdir(self.load_dir):
                file_path = os.path.join(self.load_dir, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                except Exception as e:
                    print(f'Ошибка при удалении файла {file_path}. {e}')

    def __call__(self, Simulation_loop_handler):

        img = Simulation_loop_handler.Robot.Get_camera_image()
        Simulation_loop_handler.loop_memory_dict['pre_last_gotten_image'] = Simulation_loop_handler.loop_memory_dict.get('last_gotten_image')
        Simulation_loop_handler.loop_memory_dict['last_gotten_image'] = img
        if self.load_dir:
            cv2.imwrite(
                f"{self.load_dir}/{round(Simulation_loop_handler.sim.getSimulationTime(), 2)}.jpg",
                img
            )