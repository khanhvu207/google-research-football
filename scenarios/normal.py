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

	def encounterEnemyGoalkeeper(self, radius):
		dist_to_enemy_goalkeeper = self.util.dist(self.playerPos, self.obs["right_team"][GOALKEEPER])
		return dist_to_enemy_goalkeeper <= radius
	
	def nearestFrontEnemy(self):
		farthest = 999
		candidate = None
		for enemy in self.obs["right_team"]:
			if self.playerPos[0] < enemy[0] and self.util.dist(enemy, self.playerPos) < farthest:
				farthest = self.util.dist(enemy, self.playerPos)
				candidate = enemy
		return candidate

	def doDefPassing(self):
		import numpy as np

		if self.obs["active"] == GOALKEEPER:
			return self.util.withSticky(Action.Shot, None, False)
		
		passType = Action.HighPass

		if abs(self.playerPos[1]) < SHOT_RANGE_Y:
			passing_choice = [Action.TopRight, Action.BottomRight]
			return self.util.withSticky(passType, np.random.choice(passing_choice), False)
		
		return self.util.withSticky(passType, Action.Right, False)
	
	def isWinning(self):
		return self.obs["score"][0] > self.obs["score"][1]

	def makeAction(self):
		import numpy as np

		if self.hasBall:
			if self.playerPos[0] < PASSING_RANGE_X:
				return self.doDefPassing()
			
			if self.playerPos[0] > 0.77 and abs(self.playerPos[1]) > 0.28:
				if self.playerPos[1] > 0:
					return self.util.withSticky(Action.HighPass, Action.TopLeft, False)
				else:
					return self.util.withSticky(Action.HighPass, Action.BottomLeft, False)

			# if self.encounterEnemyGoalkeeper(SHOT_TRIGGERING_RADIUS):
			# 	return self.util.withSticky(Action.Shot, None, False)

			if self.insideShotRange(self.playerPos):
				return self.util.withSticky(Action.Shot, None, False)
			
			elif abs(self.obs["right_team"][GOALKEEPER][0] - 1) > GOALIE_OUT and self.playerPos[0] > LONG_SHOT_X and abs(self.playerPos[1]) < LONG_SHOT_Y:
				return self.util.withSticky(Action.Shot, None, False)
				
			else:
				direction = self.util.runTowardTarget(self.playerPos, ENEMY_GOAL)
				return self.util.withSticky(None, direction, True)
		else:
			ball_landing_pos = self.util.ballLandingPos(self.obs["ball"], self.obs["ball_direction"]) if self.obs["ball"][2] > PICK_HEIGHT else self.obs["ball"]
			direction = self.util.runTowardTarget(self.playerPos, ball_landing_pos)
			return self.util.withSticky(None, direction, True)