from robolab_turtlebot import Turtlebot, Rate, get_time
import sys
import math as m
import tube_seg as seg
import help_func as help
import vypocet as vyp
import cv2

turtle = Turtlebot(pc=True, rgb = True)
rate = Rate(100)
sec = help.Security() 

WINDOW = "test"


def rot_30_deg(turtle):
    t = get_time()
    rate = Rate(100)
    while not turtle.is_shutting_down() and not sec.bumped2obst and (get_time() - t) < 1.75:
        turtle.cmd_velocity(angular=0.55)
        rate.sleep()

def scan_for_ball(turtle):
    turtle.reset_odometry()
    all = False
    imp_objects = []
    # cv2.namedWindow(WINDOW)

    yellow = 0
    blue = 0
    timeout = get_time()
    while not turtle.is_shutting_down() and not sec.bumped2obst and not all:
        turtle.wait_for_rgb_image()
        img = turtle.get_rgb_image()
        pc = turtle.get_point_cloud()

        odo = turtle.get_odometry()
        segs, mask = seg.segment_all(img, pc)
        # cv2.imshow(WINDOW, mask)    
        # cv2.waitKey(1)
        ##print("-----------")
        # print("uz jsem viděl zlutá,modrá,celkem:",yellow, blue, len(imp_objects))
        for segment in segs:
            segment.trasform_pos_pc2ref(odo)
            if segment.color == "yellow" and not vyp.already_seen(imp_objects, segment):
                found, count = get_objects(turtle, segment.color, imp_objects)
                imp_objects.extend(found)
                yellow += count
            if segment.color == "blue" and not vyp.already_seen(imp_objects, segment):
                found, count = get_objects(turtle, segment.color, imp_objects)
                blue += count
                imp_objects.extend(found)

        if blue == 2 and yellow == 1:
            all = True
        elif blue > 2 or yellow > 1:
            rot_30_deg(turtle)
            imp_objects = []
            blue = 0
            yellow = 0
        else:
            rot_30_deg(turtle)
        #if timeout + 40 > get_time():
        #    imp_objects = []
        #    yellow = 0
        #    blue = 0
        print(imp_objects)

    return imp_objects

def get_objects(turtle, color, imp_objects=[]):
    turtle.wait_for_rgb_image()
    turtle.wait_for_point_cloud()

    pc = turtle.get_point_cloud()
    img = turtle.get_rgb_image()
    odo = turtle.get_odometry()
    objects, mask = seg.segment_all(img, pc)
    res = []
    cnt = 0
    for obj in objects:
        if obj.color == color:
            obj.trasform_pos_pc2ref(odo)
            if not (m.isnan(obj.coords_2D[0]) or m.isnan(obj.coords_2D[1])) \
            and not vyp.already_seen(imp_objects, obj):
                res.append(obj)
                cnt += 1
    return res, cnt


def go(dis, max_speed, accel):
    P_go = 0.5
    min_speed = 0.1
    poss_err = 0.05
    turtle.reset_odometry()
    turtle.wait_for_odometry()
    turtle.wait_for_odometry()
    odo = turtle.get_odometry()
    err = dis - odo[0]
    prev_speed = 0
    while not turtle.is_shutting_down() and not sec.bumped2obst and err > poss_err:
        go_speed = min_speed + abs(err * P_go)
        if go_speed > max_speed:
            go_speed = max_speed
        if (go_speed - prev_speed) > accel:
            go_speed = prev_speed + accel
        prev_speed = go_speed
        turtle.cmd_velocity(linear=go_speed)
        odo = turtle.get_odometry()
        err = dis - odo[0]
        rate.sleep()
    odo = turtle.get_odometry()
    turtle.wait_for_odometry()

def rot(rot, max_rot):
    turtle.reset_odometry()
    P_rot = 1.5
    turtle.wait_for_odometry()
    turtle.wait_for_odometry()
    minus = False
    odo = turtle.get_odometry()
    if rot < 0:
        minus=True
        rot = abs(rot)
    err = rot - abs(odo[2])
    while not turtle.is_shutting_down() and not sec.bumped2obst and err > 0.01:
        rot_speed = 0.157 + abs(err * P_rot)
        if rot_speed > max_rot:
            rot_speed = max_rot
        
        if minus:
            rot_speed = -rot_speed
            turtle.cmd_velocity(angular=rot_speed)
        else:
            turtle.cmd_velocity(angular=rot_speed)
            
        turtle.cmd_velocity(angular=rot_speed)
        odo = turtle.get_odometry()
        err = rot - abs(odo[2])
        rate.sleep()

def is_all():
    all = False
    cv2.namedWindow(WINDOW)
    while not turtle.is_shutting_down() and not sec.bumped2obst and not all:
        turtle.wait_for_rgb_image()
        img = turtle.get_rgb_image()
        yellow = 0
        blue = 0
        segs, mask = seg.segment_all(img)
        cv2.imshow(WINDOW, mask)    
        cv2.waitKey(1)
        for segment in segs:
            if segment.color == "yellow":
                yellow += 1
            if segment.color == "blue":
                blue += 1
        if blue == 2 and yellow == 1:
            all = True
        else:
            turtle.cmd_velocity(angular=0.55)
        rate.sleep()
    
    turtle.wait_for_rgb_image()
    turtle.wait_for_point_cloud()

    pc = turtle.get_point_cloud()
    img = turtle.get_rgb_image()
    tubes, mask = seg.segment_all(img, pc)
    return tubes

def ball_center():
    ball = False
    rot_speed = 0.7
    while not ball:
        turtle.wait_for_rgb_image()
        img = turtle.get_rgb_image()
        segs, mask = seg.segment_all(img)
        for segment in segs:
            
            if segment.color == "yellow":
                ball = True
                rot_speed = 0
        turtle.cmd_velocity(angular=rot_speed)
        rate.sleep()

    ang_to_ball = 0
    found_angle = False

    while not found_angle:
        turtle.wait_for_rgb_image()
        turtle.wait_for_point_cloud()

        pc = turtle.get_point_cloud()
        img = turtle.get_rgb_image()
        segs, mask = seg.segment_all(img, pc)

        turtle.wait_for_odometry()
        turtle.wait_for_odometry()
        odo = turtle.get_odometry()
        for segment in segs:
            if segment.color == "yellow":
                ang_to_ball = vyp.ang_to_ball(segment.pc_pos, odo)
                found_angle = True
        if not found_angle:
            turtle.cmd_velocity(angular=rot_speed)
        rate.sleep()
    return ang_to_ball

def ball_center_cam():
    ball = False
    ball_centered = False
    osc = 0
    bf = 0
    rot_speed = 0.7
    turtle.reset_odometry()
    while not ball:
        turtle.wait_for_rgb_image()
        img = turtle.get_rgb_image()
        segs, mask = seg.segment_all(img)
        for segment in segs:
            if segment.color == "yellow":
                ball = True
                rot_speed = 0
        turtle.cmd_velocity(angular=rot_speed)
        rate.sleep()
    
    while not ball_centered:
        if osc > 10:
            rot_30_deg(turtle)
            osc = 0

        turtle.wait_for_rgb_image()
        turtle.wait_for_point_cloud()

        pc = turtle.get_point_cloud()
        img = turtle.get_rgb_image()
        segs, mask = seg.segment_all(img, pc)

        turtle.wait_for_odometry()
        turtle.wait_for_odometry()
        odo = turtle.get_odometry()
        for segment in segs:
            if segment.color == "yellow":
                turtle.cmd_velocity(angular=0)
                err = segment.pc_pos[0] - 0.015
                if err > 0.01:
                    turtle.cmd_velocity(angular=(-0.45))
                    if bf == 1:
                        osc += 1
                    bf = -1
                elif err < -0.01:
                    turtle.cmd_velocity(angular=0.52)
                    if bf == -1:
                        osc += 1
                    bf = 1
                else:
                    ball_centered = True
        rate.sleep()
    return 0

def get_img_pc(turtle):
    turtle.wait_for_rgb_image()
    turtle.wait_for_point_cloud()

    pc = turtle.get_point_cloud()
    img = turtle.get_rgb_image()
    return img, pc

def goal(dis, speed, accel):
    poss_err = 0.05
    go_speed = speed
    turtle.reset_odometry()
    turtle.wait_for_odometry()
    turtle.wait_for_odometry()
    odo = turtle.get_odometry()
    err = dis - odo[0]
    prev_speed = 0
    while not turtle.is_shutting_down() and err > poss_err:
        go_speed = speed
        if (go_speed - prev_speed) > accel:
            go_speed = prev_speed + accel
        prev_speed = go_speed
        turtle.cmd_velocity(linear=go_speed)
        odo = turtle.get_odometry()
        err = dis - odo[0]
        rate.sleep()
    turtle.cmd_velocity(linear=0)
    odo = turtle.get_odometry()
    turtle.wait_for_odometry()

def goal_dis(view):
    tube_coords = []
    turtle.wait_for_odometry()
    odo = turtle.get_odometry()
    for tube in view:
        if tube.color == "blue":
            tube.trasform_pos_pc2ref(odo)
            tube_coords.append(tube.coords_2D)
    if len(tube_coords) == 2:
        goal_mid = vyp.goal_mid(tube_coords[0], tube_coords[1])
        dis = (m.sqrt((odo[0] - goal_mid[0])**2 + (odo[1] - goal_mid[1])**2)) - 0.5
    else:   
        return 0
    return dis

def get_dist_angle(turtle, imp_objects):
    posts = []
    for obj in imp_objects:
        if obj.color == "yellow":
            ball = obj
        if obj.color == "blue":
            if obj.color == "blue":
                posts.append(obj)

    turtle.wait_for_odometry()
    turtle.wait_for_odometry()
    odo = turtle.get_odometry()
    odo_xy = [odo[0],odo[1]]

    kick_off, det_around = vyp.kick_pos(ball.coords_2D,posts[0].coords_2D,posts[1].coords_2D, odo)
    print("Kick off: ",kick_off)
    distance, angle = vyp.dist_angle(odo_xy, ball.coords_2D, kick_off)
    print("Distance, angle to kick off: ",distance, angle)

    if vyp.check_collison(imp_objects, angle, odo_xy):
        print("\n Colision detected! \n")
        distance, angle = vyp.dist_angle(odo_xy, ball.coords_2D, det_around)
        collision = True
    else:    
        print("No colision!!!")
        collision = False

    return distance, angle, collision


def is_ready(dist, collision):
    return dist < 0.13 and not collision ## If the correction is smaller than 15cm it will go for goal

def main():
    turtle = Turtlebot(pc=True, rgb = True)
    rate = Rate(100)
    turtle.reset_odometry()
 
    ## TODO - implement security feature, so that robot stops when he bumbs into something
    ## - Change in help_func self.button = False;
    turtle.register_button_event_cb(sec.button_cb)
    turtle.register_bumper_event_cb(sec.bumper_cb)
    ready2start = False

    if not len(sys.argv) > 1: 
        while not ready2start:
            ready2start = sec.button_pressed

    turtle.play_sound(2)

    turtle.wait_for_odometry()
    turtle.wait_for_odometry()

    

    max_rot = 1.57
    max_go = 0.69
    ready2goal = False
    starting_pos = True

    while   not turtle.is_shutting_down() \
            and not ready2goal and not sec.bumped2obst:
        # scan for objects
        imp_obj = scan_for_ball(turtle)
        if sec.bumped2obst:
            print("\nBumped!\n")
            break
        # claculate distance and angle to make a move
        distance, angle, collision = get_dist_angle(turtle, imp_obj)
        ready2goal = is_ready(distance, collision)
        # if is not at goaling position move according to calculated values
        if not ready2goal or starting_pos:
            starting_pos = False
            ready2goal = False
            ball_ang = ball_center()
            turtle.wait_for_odometry()
            odo = turtle.get_odometry()
            back_angle = vyp.get_ret_angle(odo, angle + ball_ang)
            rot(angle + ball_ang, max_rot)
            go(distance, max_go, 0.005)

        else:
            ## Proceed with scoring a goal
            dis = 0.60
            imp_obj = scan_for_ball(turtle)
            img, pc = get_img_pc(turtle)
            view, mask = seg.segment_all(img, pc)
            for segment in view:
                if segment.color == "yellow":
                    dis = segment.pc_pos[2] ## Distance to ball
            ball_center_cam()
            dis = goal_dis(imp_obj)
            print("Dis",dis)
            if dis > 0:
                goal(dis, 15, 0.01)
                turtle.play_sound(1)
                break
    print("\nProgram ended\n")

if __name__ == '__main__':
    main()