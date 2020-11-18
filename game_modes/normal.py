from kaggle_environments.envs.football.helpers import *
from utils import *
from consts import *
from actions import *

class Normal:
	def __init__(self, obs):
		self.Obs = obs
		self.PlayerPos = obs["left_team"][obs["active"]]
		self.HasBall = obs["ball_owned_player"] == obs["active"] and obs["ball_owned_team"] == 0
		self.Util = Utilities(obs)
	
	def makeAction(self):
		if self.PlayerPos[0] > SHOT_RANGE_X and Action.Sprint in self.Obs['sticky_actions']:
			return Action.ReleaseSprint
		elif self.PlayerPos[0] <= SHOT_RANGE_X and not Action.Sprint in self.Obs['sticky_actions']:
			return Action.Sprint

		if not self.HasBall:
			return Chase(self.Obs)
		else:
			if self.PlayerPos[0] > SHOT_RANGE_X and abs(self.PlayerPos[1]) < SHOT_RANGE_Y:
				return Shot(self.Obs)
			elif self.Util.dist(self.Obs['right_team'][GOALKEEPER_ID], ENEMY_GOAL) > LONG_SHOT and self.PlayerPos[0] > LONG_X and abs(self.PlayerPos[1]) < LONG_Y:
				return Shot(self.Obs)
			elif self.PlayerPos[0] <= PASSING_RANGE_X and EnemyApproaching(self.Obs) == True:
				return Pass(self.Obs)
			else:
				return Attack(self.Obs)