from consts import *
from utils import *
from kaggle_environments.envs.football.helpers import *

def Shot(obs):
	HelperFuncs = Utilities(obs)
	PlayerPos = obs["left_team"][obs["active"]]
	GoalPos = [1, 0]

	NextAction = Action.Shot
	NextDirection = HelperFuncs.runTowardTarget(PlayerPos, GoalPos)
	HoldSprint = False
	return HelperFuncs.withSticky(NextAction, NextDirection, HoldSprint)