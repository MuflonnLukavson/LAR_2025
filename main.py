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
    print("starting test")
    turtle.register_button_event_cb(sec.button_cb)
    turtle.register_bumper_event_cb(sec.bumper_cb)

    while not turtle.is_shutting_down() and cnt < 5:
        # get point cloud
        turtle.wait_for_point_cloud()
        turtle.wait_for_rgb_image()

        pc = turtle.get_point_cloud()
        img = turtle.get_rgb_image()


        cnt += 1
        # segments all tubes
        tubes = seg.segment_all(img, pc)
        print(tubes)
        input("--------------------")
        rate.sleep()



if __name__ == '__main__':
    main()
