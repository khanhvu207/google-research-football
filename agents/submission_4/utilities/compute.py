from agents.submission_4.consts import *
from kaggle_environments.envs.football.helpers import *

class Utilities:
	def __init__(self, obs):
		self.obs = obs
		self.directions = [[Action.TopLeft, Action.Top, Action.TopRight], 
							[Action.Left, Action.Idle, Action.Right], 
							[Action.BottomLeft, Action.Bottom, Action.BottomRight]]
		self.dirsign = lambda x: 1 if abs(x) < 0.01 else (0 if x < 0 else 2)
	
	def withSticky(self, action, direction, sprinting):
		if sprinting == True and Action.Sprint not in self.obs["sticky_actions"]:
			return Action.Sprint
		elif sprinting == False and Action.Sprint in self.obs["sticky_actions"]:
			return Action.ReleaseSprint
		if direction == None:
			return action
		if action == None:
			return direction
		return action if direction in self.obs["sticky_actions"] else direction

	def runTowardTarget(self, player_pos, target_pos):
		xdir = self.dirsign(target_pos[0] - player_pos[0])
		ydir = self.dirsign(target_pos[1] - player_pos[1])
		return self.directions[ydir][xdir]
	
	def dist(self, A, B):
		import numpy as np
		dx = A[0] - B[0]
		dy = A[1] - B[1]
		return np.sqrt(dx * dx + dy * dy)
	
	def ballLandingPos(self, ball, ball_direction):
		import numpy as np
		start_height = ball[2]
		end_height = PICK_HEIGHT
		start_speed = ball_direction[2] 
		time = np.sqrt(start_speed ** 2 / GRAVITY ** 2 - 2 / GRAVITY * (end_height - start_height)) + start_speed / GRAVITY
		return [ball[0] + ball_direction[0] * time, ball[1] + ball_direction[1] * time]