from kaggle_environments.envs.football.helpers import *
from utilities import compute
from consts import *

class KickOff:
	def __init__(self, obs):
		self.obs = obs
		self.playerPos = obs["left_team"][obs["active"]]
		self.util = compute.Utilities(obs)

	def makeKickOffAction(self):
		import numpy as np
		passing_choice = [Action.TopRight, Action.BottomRight]
		return self.util.withSticky(Action.HighPass, np.random.choice(passing_choice), False)