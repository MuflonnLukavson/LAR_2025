#!/usr/bin/env python

from robolab_turtlebot import Turtlebot, Rate
import tube_seg as seg


x_range = (-0.3, 0.3)
z_range = (0.3, 3.0)
WINDOW = 'obstacles'


def main():

    turtle = Turtlebot(pc=True, rgb = True)
    rate = Rate(10000)

    cnt = 0
    while not turtle.is_shutting_down() and cnt < 5:
        # get point cloud
        pc = turtle.get_point_cloud()
        img = turtle.get_rgb_image()

        if pc or img is None:
            continue
        cnt += 1
        seg.segment_all_tubes(img, pc)
        print("-------------------------")
        rate.sleep()



if __name__ == '__main__':
    main()
