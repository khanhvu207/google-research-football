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
		dist_to_goal = self.util.dist(pos, ENEMY_GOAL)
		return dist_to_goal < SHOT_RANGE_RADIUS

	def makeAction(self):
		# Make sure the player is sprinting while he is inside the SPRINT_RANGE
		if 0 < self.playerPos[0] < SPRINT_RANGE and Action.Sprint not in self.obs["sticky_actions"]:
			return Action.Sprint
		elif SPRINT_RANGE < self.playerPos[0] and Action.Sprint in self.obs["sticky_actions"]:
			return Action.ReleaseSprint
		
		if self.hasBall:
			if self.insideShotRange(self.playerPos):
				return Action.Shot
			elif abs(self.obs["right_team"][GOALKEEPER][0] - 1) > GOALIE_OUT and self.playerPos[0] > LONG_SHOT_X and abs(self.playerPos[1]) < LONG_SHOT_Y:
				return Action.Shot
			else:
				return self.util.runTowardTarget(self.playerPos, ENEMY_GOAL)
		else:
			ball_landing_pos = self.obs["ball"]
			return self.util.runTowardTarget(self.playerPos, ball_landing_pos)