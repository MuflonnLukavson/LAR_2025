# Working with objects and their purpouse
import math as m
import numpy as np
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
            self.test = self.trasform_pos_pc2ref()
        else:
            self.pc_pos = None

    def __repr__(self):
        return f"{self.color}, im_center: {self.im_center_pos}, point_cloud: {self.pc_pos}\n"

    def trasform_pos_pc2ref(self):
        #TODO
        theta = 0
        t1, t2 = 0, 0
        c, s = np.cos(theta), np.sin(theta)
        print(c,s)
        R_matrix = np.array((c , -s),(s, c))
        H_matrix = np.array((c, -s, t1),(s, c, t2),(0,0,1))
        print(R_matrix, H_matrix)
        pass

    
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
    
