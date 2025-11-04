from  Default_interfaces import Default_node_interface
import cv2

class IMAGE_SHOWER(Default_node_interface):
    def __init__(self, params=None):
        pass

    def __call__(self, Simulation_loop_handler):
        cv2.imshow("Frame", Simulation_loop_handler.loop_memory_dict['last_gotten_image'])
        cv2.waitKey(1)