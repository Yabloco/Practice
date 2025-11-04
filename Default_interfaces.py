from abc import ABC, abstractmethod

class Default_robot_interface(ABC):
    def __init__(self, paths=None, simulation=None):
        self.sim = simulation
        self.linear_velocity = 0
        self.rotational_velocity = 0
        self.sidewalk_velocity = 0

    @abstractmethod
    def UPDATE_VEL(self):
        pass

    def Set_linear_velocity(self, value):
        self.linear_velocity = value
        self.UPDATE_VEL()

    def Set_rotational_velocity(self, value):
        self.rotational_velocity = value
        self.UPDATE_VEL()

    def Set_sidewalk_velocity(self, value):
        self.sidewalk_velocity = value
        self.UPDATE_VEL()

    @abstractmethod
    def Get_camera_image(self):
        pass

    @abstractmethod
    def Get_camera_real_cords(self):
        pass

class Default_node_interface(ABC):
    @abstractmethod
    def __init__(self, params=None):
        pass

    @abstractmethod
    def __call__(self, Simulation_loop_handler, values=None):
        pass