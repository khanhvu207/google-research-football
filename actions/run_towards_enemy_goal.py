from consts import *
from utils import *
from kaggle_environments.envs.football.helpers import *
from sklearn.ensemble import RandomForestClassifier
import math

def get_distance(pos1,pos2):
    return ((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2)**0.5

def get_heading(pos1,pos2):
    raw_head=math.atan2(pos1[0]-pos2[0],pos1[1]-pos2[1])/math.pi*180

    if raw_head<0:
        head=360+raw_head
    else:
        head=raw_head
    return head

def get_action(action_num):
    if action_num==0:
        return Action.Idle
    if action_num==1:
        return Action.Left
    if action_num==2:
        return Action.TopLeft
    if action_num==3:
        return Action.Top
    if action_num==4:
        return Action.TopRight
    if action_num==5:
        return Action.Right
    if action_num==6:
        return Action.BottomRight
    if action_num==7:
        return Action.Bottom
    if action_num==8:
        return Action.BottomLeft
    if action_num==9:
        return Action.LongPass
    if action_num==10:
        return Action.HighPass
    if action_num==11:
        return Action.ShortPass
    if action_num==12:
        return Action.Shot
    if action_num==13:
        return Action.Sprint
    if action_num==14:
        return Action.ReleaseDirection
    if action_num==15:
        return Action.ReleaseSprint
    if action_num==16:
        #return Action.Sliding
        return Action.Idle
    if action_num==17:
        return Action.Dribble
    if action_num==18:
        #return Action.ReleaseDribble
        return Action.Idle
    return Action.Right

def Attack(obs):
	controlled_player_pos = obs['left_team'][obs['active']]
	x = controlled_player_pos[0]
	y = controlled_player_pos[1]

	dat=[]
	to_append=[]
	controlled_player_pos = obs['left_team'][obs['active']]

	goalx=0.0
	goaly=0.0

	sidelinex=0.0
	sideliney=0.42

	goal_dist=get_distance((x,y),(goalx,goaly))
	sideline_dist=get_distance((x,y),(sidelinex,sideliney))
	to_append.append(goal_dist)
	to_append.append(sideline_dist)

	for i in range(len(obs['left_team'])):
		dist=get_distance((x,y),(obs['left_team'][i][0],obs['left_team'][i][1]))
		head=get_heading((x,y),(obs['left_team'][i][0],obs['left_team'][i][1]))
		to_append.append(dist)
		to_append.append(head)
		
	for i in range(len(obs['right_team'])):
		dist=get_distance((x,y),(obs['right_team'][i][0],obs['right_team'][i][1]))
		head=get_heading((x,y),(obs['right_team'][i][0],obs['right_team'][i][1]))
		to_append.append(dist)
		to_append.append(head)

	dat.append(to_append)
	predicted=model.predict(dat)

	do=get_action(predicted)

	if do == None:
		return Action.Right
	else:
		return do
