from  Default_interfaces import Default_node_interface
import keyboard

class KEYBOARD_REMOTE_CONTROLLER(Default_node_interface):
    def __init__(self, params=None):
        self.velocity_multiplier = params[0]

    def __call__(self, Simulation_loop_handler):
        if keyboard.is_pressed('w'):
            Simulation_loop_handler.Robot.Set_linear_velocity(self.velocity_multiplier)
        elif keyboard.is_pressed('s'):
            Simulation_loop_handler.Robot.Set_linear_velocity(-self.velocity_multiplier)
        else:
            Simulation_loop_handler.Robot.Set_linear_velocity(0)
        if keyboard.is_pressed('a'):
            Simulation_loop_handler.Robot.Set_sidewalk_velocity(-self.velocity_multiplier)
        elif keyboard.is_pressed('d'):
            Simulation_loop_handler.Robot.Set_sidewalk_velocity(self.velocity_multiplier)
        else:
            Simulation_loop_handler.Robot.Set_sidewalk_velocity(0)
        if keyboard.is_pressed('q'):
            Simulation_loop_handler.Robot.Set_rotational_velocity(self.velocity_multiplier)
        elif keyboard.is_pressed('e'):
            Simulation_loop_handler.Robot.Set_rotational_velocity(-self.velocity_multiplier)
        else:
            Simulation_loop_handler.Robot.Set_rotational_velocity(0)