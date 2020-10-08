import numpy as np
from kaggle_environments.envs.football.helpers import *

@human_readable_agent
def agent(obs):
	return Action.Idle