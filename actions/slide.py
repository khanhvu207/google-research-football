from consts import *
from utils import *
from kaggle_environments.envs.football.helpers import *

def CanSlide(obs, player):
	if obs['ball_owned_team'] != 1:
		return False

	HelperFuncs = Utilities(obs)

	opp = obs['right_team'][obs['ball_owned_player']]
	opp_dir = obs['right_team_direction'][obs['ball_owned_player']]
	player_dir = obs['left_team_direction'][obs['active']]
	opp_future = [opp[0] + opp_dir[0], opp[1] + opp_dir[1]]
	player_future = [player[0] + player_dir[0], player[1] + player_dir[1]]

	dist_to_opp = HelperFuncs.dist(player, opp)
	future_dist_to_opp = HelperFuncs.dist(player_future, opp_future)

	if player[0] > -0.65 and abs(player[1]) > 0.25 and future_dist_to_opp < 0.015 and dist_to_opp > future_dist_to_opp:
		return True
	
	return False