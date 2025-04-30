# Working with objects and their purpouse
import math as m
import numpy as np
import copy as cp
ball = 1
goal = 2
barrier = 3

class Object():
    def __init__(self, color, im_center_x, im_center_y, pc):
        self.color = color  
        # position of center of the object in the picture
        self.im_center_pos = [im_center_x, im_center_y] 
        self.coords_2D = None

        if len(pc) > 0:
            # position of the center in point cloud
            self.pc_pos = self.map_to_pc(im_center_x, im_center_y, pc) 
        else:
            self.pc_pos = None

    def __repr__(self):
        return f"{self.color}, im_center: {self.im_center_pos}, point_cloud: {self.pc_pos}, 2D: {self.coords_2D}\n"

    def trasform_pos_pc2ref(self, odo):
        print("odo:", odo)
        x,y = self.pc_pos[0], self.pc_pos[2]
        #TODO
        theta = odo[2]
        t1, t2 = odo[1], odo[0]
        c, s = np.cos(theta), np.sin(theta)
        R_matrix = np.array(((c , -s),(s, c)))
        H_matrix = np.array(((c, -s, t1),(s, c, t2),(0,0,1)))
        H_inv = np.linalg.inv(H_matrix)
        if len(self.pc_pos) > 0:
            coords = H_matrix.dot(self.pc_pos)
            coords_2 = (R_matrix).dot(([x - t1, y - t2]))

        print(coords_2) 
        self.coords_2D = cp.deepcopy(coords_2)

    def has_coords_2D(self):
        return self.coords_2D != None

    
import math as m
import numpy as np

def map_to_pc(self, im_x, im_y, pc):
    """
    Returns the average point cloud coordinates of a 5x5 neighborhood
    around (im_x, im_y). Coordinates are in meters.
    Ignores NaN values.
    """
    x = int(round(im_x))
    y = int(round(im_y))

    valid_points = []

    for i in range(5):
        for j in range(5):
            px = x + j
            py = y + i
            if 0 <= px < 640 and 0 <= py < 480:
                pos = pc[py][px]
                if not any(m.isnan(coord) for coord in pos):
                    valid_points.append(pos)

    if valid_points:
        avg_pos = np.mean(valid_points, axis=0)
        return avg_pos.tolist()
    else:
        return [float('nan'), float('nan'), float('nan')]  # or handle as needed

    
