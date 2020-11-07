from kaggle_environments.envs.football.helpers import *
from agents.submission_4.utilities import compute
from agents.submission_4.consts import *

class ThrowIn:
	def __init__(self, obs):
		self.obs = obs
		self.playerPos = obs["left_team"][obs["active"]]
		self.util = compute.Utilities(obs)

	def makeThrowInAction(self):
		if self.playerPos[1] > 0:
			return Action.Top
		else:
			return Action.Bottom