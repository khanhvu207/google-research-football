import os
import optuna
import numpy as np
from kaggle_environments import make

MY_AGENT = "/home/kvu/google-research-football/main.py"
OPPONENT_AGENT = "/home/kvu/google-research-football/dummy_agents/memory_patterns.py"
SCENARIO = "academy_run_to_score_with_keeper" # "11_vs_11_kaggle"
EPS = 10

def objective(trial):
	# os.environ["TRIGGER_PASS"] = str(trial.suggest_float("TRIGGER_PASS", 0.05, 0.4))
	# os.environ["PASSING_RANGE_X"] = str(trial.suggest_float("PASSING_RANGE_X", -0.8, 1))
	# os.environ["CENTER_ZONE"] = str(trial.suggest_float("CENTER_ZONE", 0, 0.5))

	# os.environ["SHOT_RANGE_X"] = str(trial.suggest_float("SHOT_RANGE_X", 0.6, 0.8))
	# os.environ["SHOT_RANGE_Y"] = str(trial.suggest_float("SHOT_RANGE_Y", 0.1, 0.4))
	os.environ["GK_PROX"] = str(trial.suggest_float("GK_PROX", 0, 0.2))
	
	# os.environ["NUM_STEPS_IN_FUTURE"] = str(trial.suggest_float("NUM_STEPS_IN_FUTURE", 0, 0.2))

	rewards = []
	for _ in range(EPS):
		env = make("football", configuration={"scenario_name": SCENARIO, "actTimeout": 60.0})
		result = env.run([MY_AGENT, OPPONENT_AGENT])[-1]
		rewards.append(result[0]["reward"])

	return np.sum(rewards)