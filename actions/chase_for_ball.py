from consts import *
from utils import *
from kaggle_environments.envs.football.helpers import *

def Chase(obs):
	HelperFuncs = Utilities(obs)
	PlayerPos = obs["left_team"][obs["active"]]
	BallPos = obs["ball"]

	NextAction = None
	NextDirection = HelperFuncs.runTowardTarget(PlayerPos, BallPos)
	HoldSprint = True
	return HelperFuncs.withSticky(NextAction, NextDirection, HoldSprint)