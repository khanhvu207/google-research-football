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

	def IsDefend(self):
		return self.PlayerPos[0] < PASSING_RANGE_X

	def IsRunningToGoal(self):
		return self.PlayerPos[0] < SHOT_RANGE_X

	def IsShotting(self):
		return self.PlayerPos[0] >= SHOT_RANGE_X and abs(self.PlayerPos[1]) <= SHOT_RANGE_Y
	
	def makeAction(self):
		if not self.HasBall:
			return Chase(self.Obs)
		else:
			if self.IsRunningToGoal:
				return Attack(self.Obs)

			elif self.IsShotting:
				return Shot(self.Obs)