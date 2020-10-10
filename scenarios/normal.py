from kaggle_environments.envs.football.helpers import *
from utilities import compute
from consts import *

class Normal:
	def __init__(self, obs):
		self.obs = obs
		self.playerPos = obs["left_team"][obs["active"]]
		self.hasBall = obs["ball_owned_player"] == obs["active"] and obs["ball_owned_team"] == 0
		self.util = compute.Utilities(obs)
	
	def insideShotRange(self, pos):
		return shot_range[0][0] <= self.playerPos[0] <= shot_range[0][1] and shot_range[1][0] <= self.playerPos[1] <= shot_range[1][1]

	def makeAction(self):
		import numpy as np

		if 0 < self.playerPos[0] < SPRINT_RANGE:
			if Action.Sprint not in self.obs["sticky_actions"]:
				return Action.Sprint
		elif SPRINT_RANGE < self.playerPos[0]:
			if Action.Sprint in self.obs["sticky_actions"]:
				return Action.ReleaseSprint
		
		if self.hasBall:
			if self.insideShotRange(self.playerPos):
				return self.util.withSticky(Action.Shot, Action.BottomRight)
		
			elif abs(self.obs["right_team"][GOALKEEPER][0] - 1) > GOALIE_OUT and self.playerPos[0] > LONG_SHOT_X and abs(self.playerPos[1]) < LONG_SHOT_Y:
				return Action.Shot
				
			else:
				if self.playerPos[0] > 0.6:
					return Action.BottomRight
				else:
					return self.util.runTowardTarget(self.playerPos, ENEMY_GOAL)
		else:
			ball_landing_pos = self.util.ballLandingPos(self.obs["ball"], self.obs["ball_direction"]) if self.obs["ball"][2] > PICK_HEIGHT else self.obs["ball"]
			return self.util.runTowardTarget(self.playerPos, ball_landing_pos)