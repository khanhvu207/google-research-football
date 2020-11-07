from consts import *
from utils import *
from kaggle_environments.envs.football.helpers import *

def Attack(obs):
	HelperFuncs = Utilities(obs)
	PlayerPos = obs["left_team"][obs["active"]]

	NextAction = None
	NextDirection = HelperFuncs.runTowardTarget(PlayerPos, ENEMY_GOAL)
	HoldSprint = True
	return HelperFuncs.withSticky(NextAction, NextDirection, HoldSprint)
