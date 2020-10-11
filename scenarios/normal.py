from kaggle_environments.envs.football.helpers import *
from utilities import compute
from consts import *

class Normal:
	def __init__(self, obs):
		self.obs = obs
		self.playerPos = obs["left_team"][obs["active"]]
		self.hasBall = obs["ball_owned_player"] == obs["active"] and obs["ball_owned_team"] == 0
		self.util = compute.Utilities(obs)

	def checkSticky(self, stickyAction):
		return stickyAction in self.obs["sticky_actions"]

	def insideShotRange(self, pos):
		return shot_range[0][0] <= self.playerPos[0] <= shot_range[0][1] and shot_range[1][0] <= self.playerPos[1] <= shot_range[1][1]

	def encounterFrontEnemy(self, radius):
		for enemy in self.obs["right_team"]:
			if self.playerPos[0] < enemy[0] and self.util.dist(enemy, self.playerPos) < radius:
				return True
		return False

	def makeAction(self):
		import numpy as np

		if -1 < self.playerPos[0] < SPRINT_RANGE:
			if not self.checkSticky(Action.Sprint):
				return Action.Sprint
		elif SPRINT_RANGE < self.playerPos[0]:
			if self.checkSticky(Action.Sprint):
				return Action.ReleaseSprint
		
		if self.hasBall:
			if self.playerPos[0] <= PASSING_RANGE_X and self.encounterFrontEnemy(NEED_PASSING_RADIUS):
				if abs(self.playerPos[1]) <= CENTRAL_WIDTH:
					passing_choices = [Action.TopRight, Action.BottomRight]
					return self.util.withSticky(Action.LongPass, np.random.choice(passing_choices))
				else:
					return self.util.withSticky(Action.LongPass, Action.Right)

			if self.playerPos[0] >= SPRINT_RANGE:
				if self.encounterFrontEnemy(TRIGGER_DRIBBLE_RADIUS) and not self.checkSticky(Action.Dribble):
					return Action.Dribble
				elif not self.encounterFrontEnemy(TRIGGER_DRIBBLE_RADIUS) and self.checkSticky(Action.Dribble):
					return Action.ReleaseDribble

			if self.insideShotRange(self.playerPos):
				return Action.Shot
			
			elif abs(self.obs["right_team"][GOALKEEPER][0] - 1) > GOALIE_OUT and self.playerPos[0] > LONG_SHOT_X and abs(self.playerPos[1]) < LONG_SHOT_Y:
				return Action.Shot
				
			else:
				return self.util.runTowardTarget(self.playerPos, ENEMY_GOAL)
		else:
			if self.checkSticky(Action.Dribble):
				return Action.ReleaseDribble

			ball_landing_pos = self.util.ballLandingPos(self.obs["ball"], self.obs["ball_direction"]) if self.obs["ball"][2] > PICK_HEIGHT else self.obs["ball"]
			return self.util.runTowardTarget(self.playerPos, ball_landing_pos)