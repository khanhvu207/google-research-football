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
		if self.PlayerPos[0] > 0.6 and Action.Sprint in self.Obs['sticky_actions']:
			return Action.ReleaseSprint
		elif self.PlayerPos[0] <= 0.6 and not Action.Sprint in self.Obs['sticky_actions']:
			return Action.Sprint

		if not self.HasBall:
			if CanSlide(self.Obs, self.PlayerPos):
				return Action.Slide
			
			return Chase(self.Obs)
		else:
			if self.PlayerPos[0] < -0.7:
				return self.Util.withSticky(Action.Shot, Action.Right, True)

			if self.PlayerPos[0] <= PASSING_RANGE_X:
				if ShouldPass(self.Obs, self.PlayerPos):
					return Pass(self.Obs)

				return Attack(self.Obs)

			if self.PlayerPos[0] >= SHOT_RANGE_X and abs(self.PlayerPos[1]) < SHOT_RANGE_Y:
				return Shot(self.Obs)

			# if BadAngleToShot(self.Obs, self.PlayerPos):
			# 	return self.Util.withSticky(Action.ShortPass, Action.Top if self.PlayerPos[1] > 0 else Action.Bottom, False)
			
			return Attack(self.Obs)