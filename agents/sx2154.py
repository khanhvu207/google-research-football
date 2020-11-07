import numpy as np
from kaggle_environments.envs.football.helpers import *

@human_readable_agent
def agent(obs):
    
    # Global param
    goal_threshold = 0.5
    gravity = 0.098
    pick_height = 0.5
    step_length = 0.015 # As we always sprint
    body_radius = 0.012
    slide_threshold = step_length + body_radius
    
    # Ignore drag to estimate the landing point
    def ball_landing(ball, ball_direction):
        start_height = ball[2]
        end_height = pick_height
        start_speed = ball_direction[2]
        time = np.sqrt(start_speed**2/gravity**2 - 2/gravity*(end_height-start_height)) + start_speed/gravity
        return [ball[0]+ball_direction[0]*time, ball[1]+ball_direction[1]*time]
    
    # Check whether pressing on direction buttons and take action if so
    # Else press on direction first
    def sticky_check(action, direction):
        if direction in obs['sticky_actions']:
            return action
        else:
            return direction
    
    # Find right team positions
    def_team_pos = obs['right_team']
    # Fix goalkeeper index here as PlayerRole has issues
    # Default PlayerRole [0, 7, 9, 2, 1, 1, 3, 5, 5, 5, 6]
    def_keeper_pos = obs['right_team'][0]
    
    # We always control left team (observations and actions
    # are mirrored appropriately by the environment).
    controlled_player_pos = obs['left_team'][obs['active']]
    # Get team size
    N = len(obs['left_team'])
    
    # Does the player we control have the ball?
    if obs['ball_owned_player'] == obs['active'] and obs['ball_owned_team'] == 0:
        # Kickoff strategy: short pass to teammate
        if obs['game_mode'] == GameMode.KickOff:
            return sticky_check(Action.ShortPass, Action.Top) if controlled_player_pos[1] > 0 else sticky_check(Action.ShortPass, Action.Bottom)
        # Goalkick strategy: high pass to front
        if obs['game_mode'] == GameMode.GoalKick:
            return sticky_check(Action.LongPass, Action.Right)
        # Freekick strategy: make shot when close to goal, high pass when in back field, and short pass in mid field
        if obs['game_mode'] == GameMode.FreeKick:
            if controlled_player_pos[0] > goal_threshold:
                if abs(controlled_player_pos[1]) < 0.1:
                    return sticky_check(Action.Shot, Action.Right)
                if abs(controlled_player_pos[1]) < 0.3:
                    return sticky_check(Action.Shot, Action.TopRight) if controlled_player_pos[1]>0 else sticky_check(Action.Shot, Action.BottomRight)
                return sticky_check(Action.HighPass, Action.Top) if controlled_player_pos[1]>0 else sticky_check(Action.HighPass, Action.Bottom)
            
            if controlled_player_pos[0] < -goal_threshold:
                if abs(controlled_player_pos[1]) < 0.3:
                    return sticky_check(Action.HighPass, Action.Right)
                return sticky_check(Action.HighPass, Action.Top) if controlled_player_pos[1]>0 else sticky_check(Action.HighPass, Action.Bottom)
            
            if abs(controlled_player_pos[1]) < 0.3:
                return sticky_check(Action.ShortPass, Action.Right)
            return sticky_check(Action.ShortPass, Action.Top) if controlled_player_pos[1]>0 else sticky_check(Action.ShortPass, Action.Bottom)
        # Corner strategy: high pass to goal area
        if obs['game_mode'] == GameMode.Corner:
            return sticky_check(Action.HighPass, Action.Top) if controlled_player_pos[1]>0 else sticky_check(Action.HighPass, Action.Bottom)
        # Throwin strategy: short pass into field
        if obs['game_mode'] == GameMode.ThrowIn:
            return sticky_check(Action.ShortPass, Action.Top) if controlled_player_pos[1]>0 else sticky_check(Action.ShortPass, Action.Bottom)
        # Penalty strategy: make a shot
        if obs['game_mode'] == GameMode.Penalty:
            right_actions = [Action.TopRight, Action.BottomRight, Action.Right]
            for action in right_actions:
                if action in obs['sticky_actions']:
                    return Action.Shot
            return np.random.choice(right_actions)
            
        # Defending strategy
        if controlled_player_pos[0] < -goal_threshold:
            if abs(controlled_player_pos[1]) < 0.3:
                return sticky_check(Action.HighPass, Action.Right)
            return sticky_check(Action.HighPass, Action.Top) if controlled_player_pos[1]>0 else sticky_check(Action.HighPass, Action.Bottom)
            
        # Make sure player is running.
        if Action.Sprint not in obs['sticky_actions']:
            return Action.Sprint
        
        # Shot if we are 'close' to the goal (based on 'x' coordinate).
        if controlled_player_pos[0] > goal_threshold:
            if abs(controlled_player_pos[1]) < 0.1:
                return sticky_check(Action.Shot, Action.Right)
            if abs(controlled_player_pos[1]) < 0.3:
                return sticky_check(Action.Shot, Action.TopRight) if controlled_player_pos[1]>0 else sticky_check(Action.Shot, Action.BottomRight)
            elif controlled_player_pos[0] < 0.85:
                return Action.Right
            else:
                return sticky_check(Action.HighPass, Action.Top) if controlled_player_pos[1]>0 else sticky_check(Action.HighPass, Action.Bottom)
        
        # Run towards the goal otherwise.
        return Action.Right
    else:
        # when the ball is generally on the ground not flying
        if obs['ball'][2] <= pick_height:
            # Run towards the ball's left position.
            if obs['ball'][0] > controlled_player_pos[0] + slide_threshold:
                if obs['ball'][1] > controlled_player_pos[1] + slide_threshold:
                    return Action.BottomRight
                elif obs['ball'][1] < controlled_player_pos[1] - slide_threshold:
                    return Action.TopRight
                else:
                    return Action.Right
            elif obs['ball'][0] < controlled_player_pos[0] + slide_threshold:
                if obs['ball'][1] > controlled_player_pos[1] + slide_threshold:
                    return Action.BottomLeft
                elif obs['ball'][1] < controlled_player_pos[1] - slide_threshold:
                    return Action.TopLeft
                else:
                    return Action.Left
            # When close to the ball, try to take over.
            else:
                return Action.Slide
        # when the ball is flying
        else:
            landing_point = ball_landing(obs['ball'], obs['ball_direction'])
            # Run towards the landing point's left position.
            if landing_point[0] - body_radius > controlled_player_pos[0] + slide_threshold:
                if landing_point[1] > controlled_player_pos[1] + slide_threshold:
                    return Action.BottomRight
                elif landing_point[1] < controlled_player_pos[1] - slide_threshold:
                    return Action.TopRight
                else:
                    return Action.Right
            elif landing_point[0] - body_radius < controlled_player_pos[0] + slide_threshold:
                if landing_point[1] > controlled_player_pos[1] + slide_threshold:
                    return Action.BottomLeft
                elif landing_point[1] < controlled_player_pos[1] - slide_threshold:
                    return Action.TopLeft
                else:
                    return Action.Left
            # Try to take over the ball if close to the ball.
            elif controlled_player_pos[0] > goal_threshold:
                # Keep making shot when around landing point
                return sticky_check(Action.Shot, Action.Right) if ['ball'][2] <= pick_height else Action.Idle
            else:
                return sticky_check(Action.Slide, Action.Right) if ['ball'][2] <= pick_height else Action.Idle