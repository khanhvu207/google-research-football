from kaggle_environments.envs.football.helpers import *

@human_readable_agent
def agent(obs):
    import numpy as np
    import pandas as pd
    from pandas import Series, DataFrame
    
    ###### 0. CONSTANTS ######
    
    ENEMY_TARGET = [ 1, 0]
    OWN_TARGET   = [-1, 0]

    STEP_HARD_DIST = 0.1
    STEP_EASY_DIST = 0.5 * STEP_HARD_DIST
    SAFE_DIST = 0.1

    ###### 1. SMART CONTROL: FUNCTIONS ######

    def get_action_steps(step_dist):
        import numpy as np

        return {
            Action.Idle:          [                                0,                                 0],
            Action.Left:          [step_dist * np.cos(        np.pi), step_dist * np.sin(        np.pi)],
            Action.TopLeft:       [step_dist * np.cos( 0.75 * np.pi), step_dist * np.sin( 0.75 * np.pi)],
            Action.Top:           [step_dist * np.cos( 0.5  * np.pi), step_dist * np.sin( 0.5  * np.pi)],
            Action.TopRight:      [step_dist * np.cos( 0.25 * np.pi), step_dist * np.sin( 0.25 * np.pi)],
            Action.Right:         [step_dist * np.cos(            0), step_dist * np.sin(            0)],
            Action.BottomRight:   [step_dist * np.cos(-0.25 * np.pi), step_dist * np.sin(-0.25 * np.pi)],
            Action.Bottom:        [step_dist * np.cos(-0.5  * np.pi), step_dist * np.sin(-0.5  * np.pi)],
            Action.BottomLeft:    [step_dist * np.cos(-0.75 * np.pi), step_dist * np.sin(-0.75 * np.pi)]
        }


    def get_point_point_dist(point0, point):
        import numpy as np

        x0, y0 = point0[0], point0[1]
        x, y = point[0], point[1]
        return np.sqrt((x0 - x) ** 2 + (y0 - y) ** 2)


    def correct_point(point0):
        x, y = point0[0], point0[1]
        return (-1 <= x <= 1) and (-1 <= y <= 1)


    def get_move_action_info(point0, enemy_points, step_dist=STEP_EASY_DIST):
        import numpy as np

        target_dists = {}
        for action, step in get_action_steps(step_dist).items():
            step_point = [point0[0] + step[0], point0[1] + step[1]]
            if correct_point(step_point):
                ## 1. Enemy min distance
                enemy_distances = [
                    get_point_point_dist(step_point, enemy_point)
                    for enemy_point in enemy_points
                ]
                enemy_dist = np.array(enemy_distances).min()

                ## 2. Target distance
                target_dist = get_point_point_dist(step_point, ENEMY_TARGET)

                target_dists[action] = {
                    "target_dist" : round(target_dist, 3),
                    "enemy_dist" : round(enemy_dist, 3)
                }

        return target_dists


    def get_best_move_action(get_move_action_info, safe_dist=SAFE_DIST):
        from pandas import Series

        safe_actions = {}
        for action, info in get_move_action_info.items():
            target_dist, enemy_dist = info["target_dist"], info["enemy_dist"]
            if enemy_dist >= SAFE_DIST:
                safe_actions[action] = target_dist

        if len(safe_actions) == 0:
            return Action.Right ### fix in the future

        target_action = Series(safe_actions).idxmin()

        return target_action


    def make_decision(point0, move_action_info):
        x0, y0 = point0[0], point0[1]

        ## Shot decision
        if x0 >= 0.5:
            return Action.Shot

        ## Move decision
        best_move_action = get_best_move_action(move_action_info)
        return best_move_action
    
    
    ###### 2. GAME START ######
    
    own_points = obs['left_team']
    enemy_points = obs['right_team']
    point0 = obs['left_team'][obs['active']]
    
    if Action.Sprint not in obs['sticky_actions']:
        return Action.Sprint

    if obs['ball_owned_player'] == obs['active'] and obs['ball_owned_team'] == 0:
        ###### OFFENSE: SMART CONTROL ######
        move_action_info = get_move_action_info(point0, enemy_points)
        return make_decision(point0, move_action_info)
    else:
        ###### DEFENCE: OLD STRATEGY ######
        if obs['ball'][0] > point0[0] + 0.05:
            return Action.Right
        if obs['ball'][0] < point0[0] - 0.05:
            return Action.Left
        if obs['ball'][1] > point0[1] + 0.05:
            return Action.Bottom
        if obs['ball'][1] < point0[1] - 0.05:
            return Action.Top
        return Action.Slide