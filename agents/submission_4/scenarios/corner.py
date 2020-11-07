from kaggle_environments.envs.football.helpers import *
from agents.submission_4.utilities import compute

class Corner:
	def __init__(self, obs):
		self.obs = obs
		self.util = compute.Utilities(obs)
		self.playerPos = obs["left_team"][obs["active"]]

	def makeCornerAction(self):
		if self.playerPos[1] > 0:
			return self.util.withSticky(Action.ShortPass, Action.TopLeft, False)
		else:
			return self.util.withSticky(Action.ShortPass, Action.BottomLeft, False)