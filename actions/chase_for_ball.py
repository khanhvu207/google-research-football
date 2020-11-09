from consts import *
from utils import *
from kaggle_environments.envs.football.helpers import *

def Chase(obs):
	HelperFuncs = Utilities(obs)
	PlayerPos = obs["left_team"][obs["active"]]
	BallPos = obs["ball"]
	BallDir = obs["ball_direction"]
	FutureBallPos = BallPos

	# Predict the next position of the ball
	if BallPos[2] > PICK_HEIGHT:
		FutureBallPos = HelperFuncs.ballLandingPos(BallPos, BallDir)
	else:
		FutureBallPos = [BallPos[0] + NUM_STEPS_IN_FUTURE * BallDir[0], 
						BallPos[1] + NUM_STEPS_IN_FUTURE * BallDir[1],
						BallPos[2] + NUM_STEPS_IN_FUTURE * BallDir[2]]

	NextAction = None
	NextDirection = HelperFuncs.runTowardTarget(PlayerPos, FutureBallPos)
	HoldSprint = True
	return HelperFuncs.withSticky(NextAction, NextDirection, HoldSprint)