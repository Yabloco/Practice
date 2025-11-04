from Simulation_loop_handler import Simulation_loop_handler
from Agents import Walker
import Simulation_attributes as SA

walker = Walker(paths=[SA.sim.getObject("./Walker/Right_front_joint"),
                       SA.sim.getObject("./Walker/Right_rear_joint"),
                       SA.sim.getObject("./Walker/Left_front_joint"),
                       SA.sim.getObject("./Walker/Left_rear_joint"),
                       SA.sim.getObject("./Walker/Cam"),
                       SA.sim.getObject("./Walker/Cam/dummy")],
                simulation=SA.sim)

MAIN_SIM = Simulation_loop_handler(Default_robot_interface=walker,
                                   Sim_loop_nodes=SA.NODES,
                                   simulation=SA.sim)
MAIN_SIM.start()