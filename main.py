#!/usr/bin/env python
# This file is to test segmentation and its linkage to point cloud

from robolab_turtlebot import Turtlebot, Rate
import tube_seg as seg
import help_func

def main():

    turtle = Turtlebot(pc=True, rgb = True)
    rate = Rate(100)

    sec = help_func.Security()
    cnt = 0

    # waiting for cp and rgb init
    turtle.wait_for_point_cloud()
    turtle.wait_for_rgb_image()
    print("starting test")

    turtle.register_button_event_cb(sec.button_cb)
    turtle.register_bumper_event_cb(sec.bumper_cb)

    while not turtle.is_shutting_down() and sec.button_pressed and cnt < 5:
        # get point cloud

        pc = turtle.get_point_cloud()
        img = turtle.get_rgb_image()


        # segmenting everything
        tubes = seg.segment_all(img, pc)
        odo = turtle.get_odometry()
        print(f"Odo: {odo}")
        print(tubes)
    
        if len(tubes) > 0:
            tubes[0].trasform_pos_pc2ref(odo)
        input("--------------------")

        cnt += 1
        rate.sleep()



if __name__ == '__main__':
    main()
