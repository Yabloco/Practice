class Simulation_loop_handler:
    def __init__(self, Default_robot_interface, Sim_loop_nodes, simulation):

        self.Robot = Default_robot_interface
        self.Sim_loop_nodes = Sim_loop_nodes
        self.loop_memory_dict = dict()
        self.sim = simulation
        self.running = False
        self.counter = 0

    def start(self):

        self.sim.startSimulation()
        self.running = True
        while self.running:
            for node_i in range(len(self.Sim_loop_nodes)):
                if not self.counter % self.Sim_loop_nodes[node_i][1]:
                    if potential_return := self.Sim_loop_nodes[node_i][0](self):
                        self.loop_memory_dict[potential_return[0]] = potential_return[1]
            self.sim.step()
            self.counter += 1
            print(f'Simulation time: {self.sim.getSimulationTime():.2f} [s]', sep='', end='\r')

        self.sim.stopSimulation()
        self.loop_memory_dict.clear()