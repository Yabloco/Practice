from  Default_interfaces import Default_robot_interface
import numpy as np
import cv2

class Walker(Default_robot_interface):
    def __init__(self, paths=None, simulation=None):
        super().__init__(paths, simulation)

        self.Right_front_joint = paths[0]
        self.Right_rear_joint = paths[1]
        self.Left_front_joint = paths[2]
        self.Left_rear_joint = paths[3]
        self.Cam = paths[4]
        self.Dummy = paths[5]

    def UPDATE_VEL(self):
        self.sim.setJointTargetVelocity(self.Right_front_joint,
                                        self.linear_velocity - self.rotational_velocity + self.sidewalk_velocity)
        self.sim.setJointTargetVelocity(self.Right_rear_joint,
                                        self.linear_velocity - self.rotational_velocity - self.sidewalk_velocity)
        self.sim.setJointTargetVelocity(self.Left_front_joint,
                                        self.linear_velocity + self.rotational_velocity - self.sidewalk_velocity)
        self.sim.setJointTargetVelocity(self.Left_rear_joint,
                                        self.linear_velocity + self.rotational_velocity + self.sidewalk_velocity)

    def Get_camera_image(self):
        img, resX, resY = self.sim.getVisionSensorCharImage(self.Cam)
        img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
        img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)

        return img

    def Get_camera_real_cords(self, REL_POINT=None):
        if not REL_POINT:
            REL_POINT = self.sim.getObject("./Floor")
        pos = self.sim.getObjectPosition(self.Dummy, REL_POINT)

        Z_orient = self.sim.getObjectOrientation(self.Dummy, REL_POINT)[2]
        pos.append(Z_orient)
        return pos