from kaggle_environments.envs.football.helpers import *
from utilities import compute
from consts import *

class KickOff:
	def __init__(self, obs):
		self.obs = obs
		self.playerPos = obs["left_team"][obs["active"]]
		self.util = compute.Utilities(obs)

	def makeKickOffAction(self):
		return Action.HighPass