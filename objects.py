# Working with objects and their purpouse

ball = 1
goal = 2
barrier = 3

class Object():
    def __init__(self, color, im_center_x, im_center_y, pc):
        self.color = color  # TODO
        self.im_center_pos = [im_center_x, im_center_y]

        if len(pc) > 0:
            self.pc_pos = self.map_to_pc(im_center_x, im_center_y, pc)
        else:
            self.pc_pos = None

    def __repr__(self):
        return f"{self.color}, im_center: {self.im_center_pos}, pc_center: {self.pc_pos}\n"
    

    def trasform_pos_im2ref(self):
        #TODO
        pass

    def map_to_pc_im(self, pc):
        "maps cetner to pointcloud (argument: pointcloud)"
        # pc x,y,z - image x, image y, how far it is
        x, y = self.im_center_pos
        return [pc[y][x]]
    
    def map_to_pc(self, im_x, im_y, pc):
        x = int(round(im_x))
        y = int(round(im_y))
        print(x,y)  
        res_pos = []
        for i in range(5):
            for j in range(5):
                if y + i < 480 and x + j < 640:
                    print(pc[y + i][x + j])
                    pos = pc[y+i][x+j]
                    if len(pos) == 0 or res_pos[2] < pos[2]:
                        res_pos = pos
                    else:
                        pass
        return res_pos