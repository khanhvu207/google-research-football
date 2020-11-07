import os
import optuna
import numpy as np
from kaggle_environments import make

MY_AGENT = "/home/kvu/google-research-football/main.py"
OPPONENT_AGENT = "/home/kvu/google-research-football/dummy_agents/memory_patterns.py"
EPS = 5
TRIALS = 20

def objective(trial):
	# os.environ["PASSING_RANGE_X"] = str(trial.suggest_float("PASSING_RANGE_X", -1.0, 0))
	os.environ["SHOT_RANGE_X"] = str(trial.suggest_float("SHOT_RANGE_X", 0.5, 1.0))
	os.environ["SHOT_RANGE_Y"] = str(trial.suggest_float("SHOT_RANGE_Y", 0, 0.5))
	
	rewards = []
	for _ in range(EPS):
		env = make("football", configuration={"scenario_name": "11_vs_11_kaggle"})
		result = env.run([MY_AGENT, OPPONENT_AGENT])
		rewards.append(result[-1][0]["reward"])
	
	return np.mean(rewards)