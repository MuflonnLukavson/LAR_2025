from robolab_turtlebot import Turtlebot, Rate, get_time
import sys
import math as m
import tube_seg as seg
import help_func as help
import vypocet as vyp
import cv2

turtle = Turtlebot(pc=True, rgb = True)
rate = Rate(100)

WINDOW = "test"


def rot_30_deg(turtle):
    t = get_time()
    rate = Rate(100)
    while (get_time() - t) < 1.75:
        turtle.cmd_velocity(angular=0.55)
        rate.sleep()

def scan_for_ball(turtle):

    all = False
    imp_objects = []
    # cv2.namedWindow(WINDOW)
    ang_vel = 0.55
    yellow = 0
    blue = 0
    while not all:
        turtle.wait_for_rgb_image()
        img = turtle.get_rgb_image()
        pc = turtle.get_point_cloud()

        odo = turtle.get_odometry()
        segs, mask = seg.segment_all(img, pc)
        # cv2.imshow(WINDOW, mask)    
        # cv2.waitKey(1)
        for segment in segs:
            segment.trasform_pos_pc2ref(odo)
            print("seg:",segment)
            if segment.color == "yellow" and not vyp.already_seen(imp_objects, segment):
                found, count = get_objects(turtle, segment.color)
                imp_objects.extend(found)
                yellow += count
            if segment.color == "blue" and not vyp.already_seen(imp_objects, segment):
                found, count = get_objects(turtle, segment.color)
                blue += count
                imp_objects.extend(found)
                ang_vel = -ang_vel
        print("--------------------", imp_objects)
        if blue == 2 and yellow == 1:
            all = True
        else:
            rot_30_deg(turtle)
    
    print(imp_objects)
    return imp_objects

def get_objects(turtle, color):
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
    while err > poss_err:
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

def go_new(x, y, max_speed): 
    P_go = 0.5
    accel = 0.005
    min_speed = 0.1
    poss_err = 0.09
    turtle.wait_for_odometry()
    turtle.wait_for_odometry()
    odo = turtle.get_odometry()
    err = m.sqrt((x - odo[0])**2 + (y - odo[1])**2)
    prev_speed = 0
    cnt = 0
    while err > poss_err:
        go_speed = min_speed + abs(err * P_go)
        if go_speed > max_speed:
            go_speed = max_speed
        if (go_speed - prev_speed) > accel:
            go_speed = prev_speed + accel
        prev_speed = go_speed
        turtle.cmd_velocity(linear=go_speed)
        odo = turtle.get_odometry()
        old_err = err
        err = m.sqrt((x - odo[0])**2 + (y - odo[1])**2)
        if old_err < err:
            cnt += 1

        if cnt > 5:
            print("Přejel jsem to")
            return 1
        #print(cnt)
        rate.sleep()
    return 0

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
    while err > 0.1:
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

def rot_new(rot, max_rot):
    P_rot = 1.5
    min_rot = 0.2
    turtle.wait_for_odometry()
    turtle.wait_for_odometry()
    minus = False
    odo = turtle.get_odometry()
    want = odo[2] + rot
    if rot < 0:
        minus=True
    if want > m.pi:
        want = want - (2 * m.pi)
    elif want < -m.pi:
        want = want + (2 * m.pi)
        
    err = want - odo[2]
    while err > 0.01 or err < -0.01:
        rot_speed = min_rot + abs(err * P_rot)
        if rot_speed > max_rot:
            rot_speed = max_rot
        
        if minus:
            rot_speed = -rot_speed
            turtle.cmd_velocity(angular=rot_speed)
        else:
            turtle.cmd_velocity(angular=rot_speed)
            
        turtle.cmd_velocity(angular=rot_speed)
        odo = turtle.get_odometry()
        err = want - odo[2]
        rate.sleep()

def is_all():
    all = False
    cv2.namedWindow(WINDOW)
    while not all:
        turtle.wait_for_rgb_image()
        img = turtle.get_rgb_image()
        yellow = 0
        blue = 0
        segs, mask = seg.segment_all(img)
        cv2.imshow(WINDOW, mask)    
        cv2.waitKey(1)
        for segment in segs:
            print(segment.color)
            if segment.color == "yellow":
                yellow += 1
            if segment.color == "blue":
                blue += 1
        print("--------------------")
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
            print(segment.color)
            
            if segment.color == "yellow":
                ball = True
                print("!!!!ted!!!!!")
                rot_speed = 0
        turtle.cmd_velocity(angular=rot_speed)
        print("------------")
        rate.sleep()

    turtle.wait_for_rgb_image()
    turtle.wait_for_point_cloud()

    pc = turtle.get_point_cloud()
    img = turtle.get_rgb_image()
    segs, mask = seg.segment_all(img, pc)

    print(segs)
    input()

    turtle.wait_for_odometry()
    turtle.wait_for_odometry()
    odo = turtle.get_odometry()
    ang_to_ball = 0
    for segment in segs:
        if segment.color == "yellow":
            ang_to_ball = vyp.ang_to_ball(segment.pc_pos, odo)
    return ang_to_ball

def main():
    turtle.reset_odometry()

    turtle.wait_for_odometry()
    turtle.wait_for_odometry()

    max_rot = 1.57
    max_go = 0.69

    tubes = get_objects(turtle)
    print(tubes)
    for tube in tubes:
        if tube.color == "yellow":
            ball = tube
        if tube.color == "blue":
            if 'tube1' not in locals():
                tube1 = tube
            else:
                tube2 = tube
    
    turtle.wait_for_odometry()
    turtle.wait_for_odometry()
    odo = turtle.get_odometry()
    
    kick_off = vyp.kick_pos(ball.coords_2D,tube1.coords_2D,tube2.coords_2D, odo)
    distance, angle = vyp.dist_angle([0,0], ball.coords_2D, kick_off)
    print("uhel: ", angle*(180/m.pi))
    print("------")
    print("dist: ", distance)

    ball_ang = ball_center()
    print("uhel: ", (ball_ang+angle)*(180/m.pi))
    input()
    rot_new(ball_ang + angle, max_rot)

    go(distance, max_go, 0.005)

    ball_ang = ball_center()
    print("uhel: ", ball_ang*(180/m.pi))
    input()
    rot_new(ball_ang, max_rot)
    go(1, 1, 0.02)


if __name__ == '__main__':
    main()