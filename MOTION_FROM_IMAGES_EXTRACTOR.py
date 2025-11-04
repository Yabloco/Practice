from  Default_interfaces import Default_node_interface
import cv2
import numpy as np
from scipy.spatial import cKDTree

class MOTION_FROM_IMAGES_EXTRACTOR(Default_node_interface):
    def __init__(self, params=None):
        self.orb_extractor = cv2.ORB_create(
            nfeatures=800,  # Макс. число ключевых точек
            scaleFactor=1.2,  # Шаг пирамиды
            nlevels=8,  # Число уровней в пирамиде
            edgeThreshold=31,  # Порог фильтрации у краёв
            firstLevel=0,
            WTA_K=2,  # Для BRIEF (2 — норма)
            scoreType=cv2.ORB_HARRIS_SCORE,  # или ORB_FAST_SCORE
            patchSize=31
        )

    def estimate_camera_motion(self, keypoints1, keypoints2, descriptors1, descriptors2, K):
        tree = cKDTree(descriptors2) # Создаем дерево кД для быстрого поиска ближайших соседей
        distances, indices = tree.query(descriptors1, k=2)
        good_matches = []
        for idx, (dist1, dist2) in enumerate(zip(distances[:, 0], distances[:, 1])):
            if dist1 < 0.8 * dist2: # Применяем тест Лоу для фильтрации соответствий
                good_matches.append((keypoints1[idx], keypoints2[indices[idx][0]]))
        src_pts = np.float32([kp1.pt for kp1, _ in good_matches]) # Преобразуем соответствия в массивы координат
        dst_pts = np.float32([kp2.pt for _, kp2 in good_matches])

        src_pts_norm = cv2.undistortPoints(
            src_pts.reshape(-1, 1, 2),
            K,
            None,
            P=K
        ).reshape(-1, 2) # Преобразуем точки в нормализованное пространство камеры
        dst_pts_norm = cv2.undistortPoints(
            dst_pts.reshape(-1, 1, 2),
            K, None,
            P=K).reshape(-1, 2)

        E, _ = cv2.findEssentialMat(
            src_pts_norm, dst_pts_norm,
            K,
            method=cv2.LMEDS,
            prob=0.99,
            threshold=1.0
        ) # Вычисляем эссенциальную матрицу
        _, R, T, _ = cv2.recoverPose(
            E,
            src_pts_norm,
            dst_pts_norm,
            K
        ) # Декомпозируем эссенциальную матрицу для получения R и t
        return R, T

    def __call__(self, Simulation_loop_handler):
        if Simulation_loop_handler.loop_memory_dict.get('pre_last_gotten_image') is None:
            return None
        old_keypoints, old_descriptors = self.orb_extractor.detectAndCompute(
            cv2.cvtColor(
                Simulation_loop_handler.loop_memory_dict.get('pre_last_gotten_image'),
                cv2.COLOR_BGR2GRAY
            ),
            None
        )
        new_keypoints, new_descriptors = self.orb_extractor.detectAndCompute(
            cv2.cvtColor(
                Simulation_loop_handler.loop_memory_dict.get('last_gotten_image'),
                cv2.COLOR_BGR2GRAY
            ),
            None
        )
        if not len(old_keypoints) or not len(new_keypoints):
            return None
        focal_length = Simulation_loop_handler.loop_memory_dict.get('pre_last_gotten_image').shape[1]
        K = np.array(
            [[focal_length,            0, focal_length / 2],
             [           0, focal_length, focal_length / 2],
             [           0,            0,                1]]
        )
        R, T = self.estimate_camera_motion(
            old_keypoints,
            new_keypoints,
            old_descriptors,
            new_descriptors,
            K
        )
        Simulation_loop_handler.loop_memory_dict['last_calculated_relative_motion'] = (R, T)