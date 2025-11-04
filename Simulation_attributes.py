import Nodes
from coppeliasim_zmqremoteapi_client import RemoteAPIClient

client = RemoteAPIClient()
sim = client.require('sim')
client.setStepping(True)

sim_time_limiter = Nodes.SIM_TIME_LIMIT_CHECKER([60])
keyboard_input_controller = Nodes.KEYBOARD_REMOTE_CONTROLLER([5])
im_loader = Nodes.IMAGE_LOADER(["./images_from_cam"])
tpg = Nodes.TRUE_POS_GETTER(['True_path.csv', sim.getObject("./START_POS")])
im_show = Nodes.IMAGE_SHOWER()
pl_show = Nodes.POSITION_PLOTER()
r_pl_show = Nodes.RECONSTRUCTED_POSITION_PLOTER()
mfie = Nodes.MOTION_FROM_IMAGES_EXTRACTOR()
tr = Nodes.TRAJECTORY_RECONSTRUCTOR(['Reconstructed_path.csv'])
vec = Nodes.VISUAL_EMBEDDING_CALCULATOR(['ViT_embeddings.csv'])

NODES = [(sim_time_limiter, 1),
         (im_loader,5),
         (mfie,5),
         (tr,5),
         (vec, 10),
         (keyboard_input_controller,1),
         (tpg,1),
         (im_show,5),
         (pl_show,5),
         (r_pl_show,5)]
