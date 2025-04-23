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

        if len(pc) > 0:
            # position of the center in point cloud
            self.pc_pos = self.map_to_pc(im_center_x, im_center_y, pc) 
            self.coords_2D = None
        else:
            self.pc_pos = None

    def __repr__(self):
        return f"{self.color}, im_center: {self.im_center_pos}, point_cloud: {self.pc_pos}, 2D: {self.coords_2D}\n"

    def trasform_pos_pc2ref(self, odo):
        x,y = self.pc_pos[0], self.pc_pos[2]
        #TODO
        theta = odo[2]
        t1, t2 = odo[0], odo[1]
        c, s = np.cos(theta), np.sin(theta)
        print(c,s)
        R_matrix = np.array(((c , -s),(s, c)))
        H_matrix = np.array(((c, -s, t1),(s, c, t2),(0,0,1)))
        print("R, M:",R_matrix, H_matrix, sep = "\n")
        if len(self.pc_pos) > 0:
            print(H_matrix, self.pc_pos)
            coords = H_matrix.dot(self.pc_pos)
            print([x - t1, y - t2])
            coords_2 = np.transpose(R_matrix).dot(([x - t1, y - t2]))

        print(coords, coords_2) 
        self.coords_2D = cp.deepcopy(coords)

    
    def map_to_pc(self, im_x, im_y, pc):
        """
        Gets minumum distanced coords of 5x5 surrounding pixels
        values are in meters
        """
        # TODO sometimes returns NaN - is it a problem?
        x = int(round(im_x))
        y = int(round(im_y))
        # print(x,y)  
        res_pos = []
        for i in range(5):
            for j in range(5):
                if y + i < 480 and x + j < 640:
                    # print(pc[y + i][x + j])
                    pos = pc[y+i][x+j]
                    if (len(res_pos) == 0 or res_pos[2] > pos[2]) \
                        and not (m.isnan(pos[2])):
                        # asigning pointcould position
                        res_pos = pos
                    else:
                        pass
        return res_pos
    
