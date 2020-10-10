from kaggle_environments.envs.football.helpers import *

class FreeKick:
	def __init__(self, obs):
		self.obs = obs
	
	def makeFreeKickAction(self):
		return Action.Shot