from  Default_interfaces import Default_node_interface

class SIM_TIME_LIMIT_CHECKER(Default_node_interface):
    def __init__(self, params=None):
        self.time_limit = params[0]

    def __call__(self, Simulation_loop_handler):
        if Simulation_loop_handler.sim.getSimulationTime() >= self.time_limit:
            Simulation_loop_handler.running = False