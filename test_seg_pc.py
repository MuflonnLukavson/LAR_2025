#!/usr/bin/env python
# This file is to test segmentation and its linkage to point cloud

from robolab_turtlebot import Turtlebot, Rate
import tube_seg as seg




def main():

    turtle = Turtlebot(pc=True, rgb = True)
    rate = Rate(10000)

    cnt = 0
    print("starting test")
    while not turtle.is_shutting_down() and cnt < 5:
        # get point cloud
        turtle.wait_for_point_cloud()
        turtle.wait_for_rgb_image()

        pc = turtle.get_point_cloud()
        img = turtle.get_rgb_image()

        cnt += 1
        # segments all tubes
        seg.segment_all_tubes(img, pc)
        input("--------------------")
        rate.sleep()



if __name__ == '__main__':
    main()
