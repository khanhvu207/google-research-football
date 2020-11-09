from consts import *
from utils import *
from kaggle_environments.envs.football.helpers import *

def EnemyApproaching(obs):
	HelperFuncs = Utilities(obs)
	PlayerPos = obs["left_team"][obs["active"]]

	DistToNearestFrontEnemy = 111

	for Enemy in obs["right_team"]:
		if PlayerPos[0] < Enemy[0] and HelperFuncs.dist(PlayerPos, Enemy) <= DistToNearestFrontEnemy:
			DistToNearestFrontEnemy = HelperFuncs.dist(PlayerPos, Enemy)
	return DistToNearestFrontEnemy <= TRIGGER_PASS

def Pass(obs):
	HelperFuncs = Utilities(obs)
	PlayerPos = obs["left_team"][obs["active"]]

	BestDir = Action.Right
	if abs(PlayerPos[1]) <= CENTER_ZONE:
		BestDir = Action.TopRight if PlayerPos[1] > 0 else Action.BottomRight

	NextAction = Action.HighPass
	NextDirection = BestDir
	HoldSprint = True
	return HelperFuncs.withSticky(NextAction, NextDirection, HoldSprint)