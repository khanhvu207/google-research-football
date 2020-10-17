from kaggle_environments.envs.football.helpers import *
from utilities import *
from consts import *

class Normal:
	def __init__(self, obs):
		self.obs = obs
		self.playerPos = obs["left_team"][obs["active"]]
		self.hasBall = obs["ball_owned_player"] == obs["active"] and obs["ball_owned_team"] == 0
		self.util = Utilities(obs)

	def makeAction(self):
		return Action.Idle