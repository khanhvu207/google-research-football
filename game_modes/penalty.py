from kaggle_environments.envs.football.helpers import *

class Penalty:
	def __init__(self, obs):
		self.obs = obs

	def makePenaltyAction(self):
		return Action.Shot