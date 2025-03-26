#!/usr/bin/env python

from robolab_turtlebot import Turtlebot, Rate
import tube_seg as seg




def main():

    turtle = Turtlebot(pc=True, rgb = True)
    rate = Rate(10000)

    cnt = 0
    print("test")
    while not turtle.is_shutting_down() and cnt < 5:
        # get point cloud
        turtle.wait_for_point_cloud()
        turtle.wait_for_rgb_image()

        pc = turtle.get_point_cloud()
        img = turtle.get_rgb_image()

        print(pc)
        cnt += 1
        seg.segment_all_tubes(img, pc)
        print("-------------------------")
        rate.sleep()



if __name__ == '__main__':
    main()
