from kaggle_environments.envs.football.helpers import *
from utilities import compute

class Corner:
	def __init__(self, obs):
		self.obs = obs
		self.util = compute.Utilities(obs)
		self.playerPos = obs["left_team"][obs["active"]]

	def makeCornerAction(self):
		if self.playerPos[0] > 0:
			return Action.Shot
		else: 
			return Action.HighPass