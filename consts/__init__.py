import os

# # OPTUNA PARAMS
# # Passing
# TRIGGER_PASS = float(os.environ["TRIGGER_PASS"])
# PASSING_RANGE_X = float(os.environ["PASSING_RANGE_X"]) 
# CENTER_ZONE = float(os.environ["CENTER_ZONE"])
# # Shooting
# SHOT_RANGE_X = float(os.environ["SHOT_RANGE_X"]) 
# SHOT_RANGE_Y = float(os.environ["SHOT_RANGE_Y"])
# GK_PROX = float(os.environ["GK_PROX"])
# # Ball position
# NUM_STEPS_IN_FUTURE = float(os.environ["NUM_STEPS_IN_FUTURE"])

# STATIC PARAMS
# Passing 
TRIGGER_PASS = 0.3293761602990554
PASSING_RANGE_X = -0.10270158805486779
CENTER_ZONE = 0.15505470127155654
# Shooting
SHOT_RANGE_X = 0.7 #0.6567158517594331
SHOT_RANGE_Y = 0.15 #0.2125839400490282
LONG_X = 0.4
LONG_Y = 0.2
LONG_SHOT = 0.2
# Ball position
NUM_STEPS_IN_FUTURE = 5

# UNTUNABLE PARAMS
GRAVITY = 0.098
PICK_HEIGHT = 0.5
STEP_LENGTH = 0.015
BODY_RADIUS = 0.012
SLIDE_THRESHOLD = STEP_LENGTH + BODY_RADIUS
ENEMY_GOAL = [1, 0]
INF = 999
GOALKEEPER_ID = 0
MODEL_PATH = 'random_forest/model.sav'

import pickle
from sklearn.ensemble import RandomForestClassifier
model = pickle.load(open(MODEL_PATH, 'rb'))