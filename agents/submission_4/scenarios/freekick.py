from kaggle_environments.envs.football.helpers import *
from agents.submission_4.utilities import compute
from agents.submission_4.consts import *

class FreeKick:
	def __init__(self, obs):
		self.obs = obs
		self.playerPos = obs["left_team"][obs["active"]]
		self.util = compute.Utilities(obs)

	def makeFreeKickAction(self):
		import numpy as np
		if self.playerPos[0] >= SHOT_RANGE_X:
			return self.util.withSticky(Action.Shot, None, False)

		if abs(self.playerPos[1]) < SHOT_RANGE_Y:
			passing_choice = [Action.TopRight, Action.BottomRight]
			return self.util.withSticky(Action.ShortPass ,np.random.choice(passing_choice), False)
		
		return self.util.withSticky(Action.ShortPass, Action.Right, False)