def already_seen(curr_objects, new_obj): # takes array of objects and compares their position to a new object to evaluate if it is actually a new one
    ret = False
    for object in curr_objects:
        if object.color == new_obj.color and is_close(object, new_obj):
            ret = True
            break
    return ret

def is_close(obj1, obj2): # says if 2 objects are close togehter in space
    dist = math.sqrt(math.pow(obj1.pc_pos[0] - obj2.pc_pos[0],2) + math.pow(obj1.pc_pos[2]-obj2.pc_pos[2],2))
    obj1_x, obj1_y = obj1.coords_2D
    obj2_x, obj2_y = obj2.coords_2D
    dist_2D = math.sqrt(math.pow(obj1_x - obj2_x, 2) + math.pow(obj1_y - obj2_y, 2))
    print("dist:",dist_2D)
    return dist_2D < 0.5