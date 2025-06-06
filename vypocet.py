import math
import tube_seg as seg
import objects as obj
import numpy as np

kick_off_dist = 0.7 # jak daleko od míče chceme vykopávat
nuh_uh = 3 # believable distance

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
    # Gate poles cannot be closer than 0.7 meter
    return dist_2D < 0.5

def dis_between_pos(pos1, pos2):
    return math.sqrt(math.pow(pos1[0] - pos2[0], 2) + math.pow(pos1[1] - pos2[1], 2))

def goal_mid(post1,post2): # najdi střed branky
    return [post1[0] + (post2[0]-post1[0])/2, post1[1] + (post2[1]-post1[1])/2]

def ball_corr(ball,me): #bere 2d mapu jako ball
    ball_dist_vec = [ball[0]-me[0],ball[1]-me[1]]
    ball_dist = math.sqrt(math.pow(ball_dist_vec[0],2) + math.pow(ball_dist_vec[1],2))
    #ratio = ball_dist/1.1
    ratio = (ball_dist + 0.1) / ball_dist
    return [me[0] + ball_dist_vec[0]*ratio, me[1] + ball_dist_vec[1]*ratio]

def kick_pos(ball,post1,post2, me): # najdi místo výkopu
    mid = goal_mid(post1, post2)
    new_ball = ball_corr(ball, me)
    ball_mid_vec = [new_ball[0]-mid[0], new_ball[1]-mid[1]] # vektor od míče do středu branky
    ball_mid_vec_size = math.sqrt(math.pow(ball_mid_vec[0],2) + math.pow(ball_mid_vec[1],2))
    ratio = ball_mid_vec_size/kick_off_dist # poměr délky vektoru a požadované vzdálenosti od míče
    kick = [new_ball[0]+ball_mid_vec[0]/ratio, new_ball[1]+ball_mid_vec[1]/ratio]


    # Calculation of detour position
    # TODO only one detour position - might not help to get there
    det_pos = [new_ball[0]-ball_mid_vec[1]/ratio, new_ball[1]+ball_mid_vec[0]/ratio] # kdyby bylo třeba objížďka
    me2ball = [new_ball[0] - me[0], new_ball[1] - me[1]]
    me2ball_size = math.sqrt(math.pow(me2ball[0],2) + math.pow(me2ball[1],2))
    ratio_det = me2ball_size/0.5
    det_pos2= [new_ball[0] - me2ball[1] / ratio_det, new_ball[1] + me2ball[0] / ratio_det]
    det_pos3= [new_ball[0] + me2ball[1] / ratio_det, new_ball[1] - me2ball[0] / ratio_det]
    
    return kick, det_pos2, det_pos3

def ang_to_ball(ball,me): #bere pc_pos jako ball
    #new_ball = ball_corr(ball, me)
    #return -math.tan(new_ball[0]/new_ball[1]) #uhel od ted k mici
    return -math.tan(ball[0]/ball[2])

def dist_angle(me, ball, kick): # místo výkopu do úhlu(úhel od toho, když se koukáš přímo na míč) a vzdálenosti od aktuální pozice
    new_ball = ball_corr(ball, me)
    ball_dist = math.sqrt(math.pow(me[0]-new_ball[0],2) + math.pow(me[1]-new_ball[1],2))
    kick_dist = math.sqrt(math.pow(me[0]-kick[0],2) + math.pow(me[1]-kick[1],2))
    ang = math.acos((math.pow(ball_dist,2)+math.pow(kick_dist,2)-math.pow(kick_off_dist,2))/(2*ball_dist*kick_dist)) # uhel od mice k mistu
    if (new_ball[0] - me[0])*(kick[1] - me[1]) - (new_ball[1] - me[1])*(kick[0] - me[0]) < 0:
        ang = -ang
    # --old-- ang_corr =  math.tan(new_ball[0]/new_ball[1]) #uhel od ted k mistu
    return kick_dist, ang

def is_between_ball_and_goal(me, ball, goal):
    ball_goal_vect = [goal[0] - ball[0], goal[1] - ball[1]]
    ball_me_vect = [me[0] - ball[0], me[1] - ball[1]]

    skal = ball_goal_vect[0]*ball_me_vect[0] + ball_goal_vect[1]*ball_me_vect[1]

    return 0 < skal

def check_collison(objects, angle,me):
    """
    Function checks if three objects are in same y axis direction
    and if the robot would colide with them according to calculated angle.
    If they are not, function returns True.
    """
    #sameside = np.sign(objects[0].coords_2D[1]) == np.sign(objects[1].coords_2D[1]) == np.sign(objects[2].coords_2D[1])
    posts = []
    for seg in objects:
        if seg.color == "yellow":
            ball = seg
        if seg.color == "blue":
            posts.append(seg)

    goal = goal_mid(posts[0].coords_2D,posts[1].coords_2D)
    between = is_between_ball_and_goal(me,ball.coords_2D,goal)
    return angle < 0.45 and between

def get_ret_angle(odo, angle):
    """
    Function which calculates the angle which
    should robot rotate to face the ball after movement
    """
    return -(odo[2] + angle)



def dist_angle_det(me, ball, kick,det): # if normal angle is < 24°(0.4 rad)
    new_ball = ball_corr(ball, me)
    ball_dist = math.sqrt(math.pow(me[0]-new_ball[0],2) + math.pow(me[1]-new_ball[1],2))
    # kick_dist = math.sqrt(math.pow(me[0]-kick[0],2) + math.pow(me[1]-kick[1],2))
    det_dist = math.sqrt(math.pow(me[0]-det[0],2) + math.pow(me[1]-det[1],2))
    det_to_kick_dist = math.sqrt(math.pow(det[0]-kick[0],2) + math.pow(det[1]-kick[1],2))
    first_ang = math.acos((math.pow(ball_dist,2)+math.pow(det_dist,2)-math.pow(kick_off_dist,2))/(2*ball_dist*det_dist))
    if (new_ball[0] - me[0])*(det[1] - me[1]) - (new_ball[1] - me[1])*(det[0] - me[0]) < 0:
        first_ang = -first_ang
    second_ang = math.acos((math.pow(kick_off_dist,2)+math.pow(det_to_kick_dist,2)-math.pow(kick_off_dist,2))/(2*kick_off_dist*det_to_kick_dist))
    if (new_ball[0] - det[0])*(kick[1] - det[1]) - (new_ball[1] - det[1])*(kick[0] - det[0]) < 0:
        second_ang = -second_ang
    return first_ang,det_dist,second_ang,det_to_kick_dist