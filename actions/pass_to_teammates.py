from consts import *
from utils import *
from kaggle_environments.envs.football.helpers import *

def ShouldPass(obs, player):
	HelperFuncs = Utilities(obs)

	for i in range(1, len(obs['right_team'])):
		dist_to_opp = HelperFuncs.dist(player, obs['right_team'][i])
		if dist_to_opp < 0.03:
			for i in range(1, len(obs['left_team'])):
				dist_to_mate = HelperFuncs.dist(player, obs['left_team'][i])
				dist_to_goal = HelperFuncs.dist(player, ENEMY_GOAL)
				if dist_to_mate < dist_to_goal:
					return True
			break

	return False

def BadAngleToShot(obs, player):
	if (abs(player[1] > 0.15) and player[0] > 0.85) or (player[0] > 0.7 and player[1] > 0.07 and obs['left_team_direction'][obs['active']][1] > 0) or (player[0] > 0.7 and player[1] < -0.07 and obs['left_team_direction'][obs['active']][1] < 0):
		return True
	
	return False