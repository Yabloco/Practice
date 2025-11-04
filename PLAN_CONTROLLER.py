from  Default_interfaces import Default_node_interface

class PLAN_CONTROLLER(Default_node_interface):
    class Motion_strategy_in_time:

        def __init__(self, time2command_list):

            self.time2command_list = time2command_list
            self.__current_instruction_number = 0

            if self.time2command_list[0][0]:
                self.time2command_list.insert(0, [0.0, [0, 0, 0]])

        def get_instruction(self, time):

            if (self.__current_instruction_number + 1 < len(self.time2command_list) and
                    time >= self.time2command_list[self.__current_instruction_number + 1][0]):
                self.__current_instruction_number += 1

            return self.time2command_list[self.__current_instruction_number][1]

    def __init__(self, params=None):
        self.strategy = params[0]

    def __call__(self, Simulation_loop_handler):
        velocities = self.strategy.get_instruction(Simulation_loop_handler.sim.getSimulationTime())

        Simulation_loop_handler.Robot.Set_linear_velocity(velocities[0])
        Simulation_loop_handler.Robot.Set_sidewalk_velocity(velocities[1])
        Simulation_loop_handler.Robot.Set_rotational_velocity(velocities[2])
