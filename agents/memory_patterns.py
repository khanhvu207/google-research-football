# start executing cells from here to rewrite submission.py

import math

def get_distance(x1, y1, x2, y2):
    """ get two-dimensional Euclidean distance """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_closest_opponent_ahead(obs, player_x, player_y):
    """ get closest opponent ahead """
    shortest_distance = None
    closest_opponent = None
    for i in range(1, len(obs["right_team"])):
        distance_to_opponent = get_distance(player_x, player_y, obs["right_team"][i][0], obs["right_team"][i][1])
        if (obs["right_team"][i][0] > player_x and
                abs(obs["right_team"][i][1] - player_y) < 0.1):
            if shortest_distance == None or distance_to_opponent < shortest_distance:
                shortest_distance = distance_to_opponent
                closest_opponent = obs["right_team"][i]
    return closest_opponent
    
# "%%writefile -a submission.py" will append the code below to submission.py,
# it WILL NOT rewrite submission.py

def close_to_goalkeeper_shot(obs, player_x, player_y):
    """ shot if close to the goalkeeper """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        opponent_goalkeeper = [
            obs["right_team"][0][0] + obs["right_team_direction"][0][0] * 10,
            obs["right_team"][0][1] + obs["right_team_direction"][0][1] * 10
        ]
        # player have the ball and located close to the goalkeeper
        if (obs["ball_owned_player"] == obs["active"] and
                obs["ball_owned_team"] == 0 and
                get_distance(player_x, player_y, opponent_goalkeeper[0], opponent_goalkeeper[1]) < 0.3):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.Shot
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_goal(obs, player_x, player_y):
    """ run towards the goal """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player is near center of the field's y axis
        if 0.05 > abs(player_y):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.Right
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_goal_top(obs, player_x, player_y):
    """ run towards the goal """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player is too far from the center of the field's y axis
        if 0.05 < player_y:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.TopRight
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_goal_bottom(obs, player_x, player_y):
    """ run towards the goal """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player is too far from the center of the field's y axis
        if -0.05 > player_y:
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.BottomRight
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_right(obs, player_x, player_y):
    """ run to the ball if it is to the right from player's position """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # ball is to the right from player's position
        if (obs["memory_patterns"]["ball_next_coords"]["x"] > player_x and
                abs(obs["memory_patterns"]["ball_next_coords"]["y"] - player_y) < 0.02):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.Right
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_left(obs, player_x, player_y):
    """ run to the ball if it is to the left from player's position """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # ball is to the left from player's position
        if (obs["memory_patterns"]["ball_next_coords"]["x"] < player_x and
                abs(obs["memory_patterns"]["ball_next_coords"]["y"] - player_y) < 0.02):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.Left
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_bottom(obs, player_x, player_y):
    """ run to the ball if it is to the bottom from player's position """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # ball is to the bottom from player's position
        if (obs["memory_patterns"]["ball_next_coords"]["y"] > player_y and
                abs(obs["memory_patterns"]["ball_next_coords"]["x"] - player_x) < 0.02):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.Bottom
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_top(obs, player_x, player_y):
    """ run to the ball if it is to the top from player's position """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # ball is to the top from player's position
        if (obs["memory_patterns"]["ball_next_coords"]["y"] < player_y and
                abs(obs["memory_patterns"]["ball_next_coords"]["x"] - player_x) < 0.02):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.Top
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_top_right(obs, player_x, player_y):
    """ run to the ball if it is to the top right from player's position """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # ball is to the top right from player's position
        if (obs["memory_patterns"]["ball_next_coords"]["x"] > player_x and
                obs["memory_patterns"]["ball_next_coords"]["y"] < player_y):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.TopRight
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_top_left(obs, player_x, player_y):
    """ run to the ball if it is to the top left from player's position """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # ball is to the top left from player's position
        if (obs["memory_patterns"]["ball_next_coords"]["x"] < player_x and
                obs["memory_patterns"]["ball_next_coords"]["y"] < player_y):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.TopLeft
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_bottom_right(obs, player_x, player_y):
    """ run to the ball if it is to the bottom right from player's position """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # ball is to the bottom right from player's position
        if (obs["memory_patterns"]["ball_next_coords"]["x"] > player_x and
                obs["memory_patterns"]["ball_next_coords"]["y"] > player_y):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.BottomRight
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def run_to_ball_bottom_left(obs, player_x, player_y):
    """ run to the ball if it is to the bottom left from player's position """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # ball is to the bottom left from player's position
        if (obs["memory_patterns"]["ball_next_coords"]["x"] < player_x and
                obs["memory_patterns"]["ball_next_coords"]["y"] > player_y):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.BottomLeft
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def idle(obs, player_x, player_y):
    """ do nothing, stickly actions are not affected (player maintains his directional movement etc.) """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        return True
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.Idle
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def far_from_goal_high_pass(obs, player_x, player_y):
    """ perform a high pass to the player on your team, if far from opponent's goal """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player have the ball and is far from opponent's goal
        if (obs["ball_owned_player"] == obs["active"] and
                obs["ball_owned_team"] == 0 and
                player_x < -0.2):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.HighPass
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def far_from_goal_shot(obs, player_x, player_y):
    """ perform a shot, if far from opponent's goal """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player have the ball and is far from opponent's goal
        if (obs["ball_owned_player"] == obs["active"] and
                obs["ball_owned_team"] == 0 and
                player_x < -0.5):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.Shot
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def far_from_goal_short_pass(obs, player_x, player_y):
    """ perform a short pass to the player on your team, if far from opponent's goal """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player have the ball and is far from opponent's goal
        if (obs["ball_owned_player"] == obs["active"] and
                obs["ball_owned_team"] == 0 and
                player_x < -0.2):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.ShortPass
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def bad_angle_short_pass(obs, player_x, player_y):
    """ performe a short pass to the player on your team, if angle to goal is inappropriate """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player have the ball, located close to the goal and angle to goal is inappropriate
        if (obs["ball_owned_player"] == obs["active"] and
                obs["ball_owned_team"] == 0 and
                abs(player_y) > 0.05 and
                player_x > 0.8):
                return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.ShortPass
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def go_around_opponent(obs, player_x, player_y):
    """ avoid closest ahead opponent by going around him """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # if player is far enough from the goal
        if (player_x < 0.4 and abs(player_y) < 0.2) or abs(player_y) < 0.05:
            # get coordinates of the closest opponent
            closest_opponent = get_closest_opponent_ahead(obs, player_x, player_y)
            if closest_opponent != None:
                if closest_opponent[1] <= player_y:
                    obs["memory_patterns"]["go_around_opponent"] = Action.BottomRight
                else:
                    obs["memory_patterns"]["go_around_opponent"] = Action.TopRight
                return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return obs["memory_patterns"]["go_around_opponent"]
    
    return {"environment_fits": environment_fits, "get_action": get_action}

def slide(obs, player_x, player_y):
    """ perform a slide (effective when not having a ball) """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # distance from the player to the current ball position
        distance_to_current_ball_position = get_distance(player_x, player_y, obs["ball"][0], obs["ball"][1])
        # distance from the player to position of the ball in the next step
        distance_to_next_ball_position = get_distance(player_x, player_y, obs["memory_patterns"]["ball_next_coords"]["x"], obs["memory_patterns"]["ball_next_coords"]["y"])
        # if the ball is at acceptable distance and is going to player's current position
        if (obs["ball_owned_team"] == 1 and
                distance_to_next_ball_position < distance_to_current_ball_position and
                distance_to_next_ball_position < 0.04 and
                distance_to_next_ball_position > 0.02 and
                (obs["ball_direction"][0] + obs["left_team_direction"][obs["active"]][0]) < 0.005 and
                (obs["ball_direction"][1] + obs["left_team_direction"][obs["active"]][1]) < 0.005):
            return True
        return False
        
    def get_action(obs, player_x, player_y):
        """ get action of this memory pattern """
        return Action.Slide
    
    return {"environment_fits": environment_fits, "get_action": get_action}
# "%%writefile -a submission.py" will append the code below to submission.py,
# it WILL NOT rewrite submission.py

def offence_memory_patterns(obs, player_x, player_y):
    """ group of memory patterns for environments in which player's team has the ball """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player have the ball
        if obs["ball_owned_player"] == obs["active"] and obs["ball_owned_team"] == 0:
            return True
        return False
        
    def get_memory_patterns(obs, player_x, player_y):
        """ get list of memory patterns """
        memory_patterns = [
            far_from_goal_shot,
            close_to_goalkeeper_shot,
            bad_angle_short_pass,
            go_around_opponent,
            run_to_goal,
            run_to_goal_top,
            run_to_goal_bottom,
            idle
        ]
        return memory_patterns
        
    return {"environment_fits": environment_fits, "get_memory_patterns": get_memory_patterns}
    
def defence_memory_patterns(obs, player_x, player_y):
    """ group of memory patterns for environments in which opponent's team has the ball """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player don't have the ball
        if obs["ball_owned_player"] != obs["active"] and obs["ball_owned_team"] != 0:
            return True
        return False
        
    def get_memory_patterns(obs, player_x, player_y):
        """ get list of memory patterns """
        memory_patterns = [
            run_to_ball_right,
            run_to_ball_left,
            run_to_ball_bottom,
            run_to_ball_top,
            run_to_ball_top_right,
            run_to_ball_top_left,
            run_to_ball_bottom_right,
            run_to_ball_bottom_left,
            idle
        ]
        return memory_patterns
        
    return {"environment_fits": environment_fits, "get_memory_patterns": get_memory_patterns}

def goalkeeper_memory_patterns(obs, player_x, player_y):
    """ group of memory patterns for goalkeeper """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        # player is a goalkeeper have the ball
        if (obs["ball_owned_player"] == obs["active"] and
                obs["ball_owned_team"] == 0 and
                obs["ball_owned_player"] == 0):
            return True
        return False
        
    def get_memory_patterns(obs, player_x, player_y):
        """ get list of memory patterns """
        memory_patterns = [
            far_from_goal_shot
        ]
        return memory_patterns
        
    return {"environment_fits": environment_fits, "get_memory_patterns": get_memory_patterns}

def other_memory_patterns(obs, player_x, player_y):
    """ group of memory patterns for all other environments """
    def environment_fits(obs, player_x, player_y):
        """ environment fits constraints """
        return True
        
    def get_memory_patterns(obs, player_x, player_y):
        """ get list of memory patterns """
        memory_patterns = [
            idle
        ]
        return memory_patterns
        
    return {"environment_fits": environment_fits, "get_memory_patterns": get_memory_patterns}   


# list of groups of memory patterns
groups_of_memory_patterns = [
    goalkeeper_memory_patterns,
    offence_memory_patterns,
    defence_memory_patterns,
    other_memory_patterns
]
# "%%writefile -a submission.py" will append the code below to submission.py,
# it WILL NOT rewrite submission.py

from kaggle_environments.envs.football.helpers import *

def find_patterns(obs, player_x, player_y):
    """ find list of appropriate patterns in groups of memory patterns """
    for get_group in groups_of_memory_patterns:
        group = get_group(obs, player_x, player_y)
        if group["environment_fits"](obs, player_x, player_y):
            return group["get_memory_patterns"](obs, player_x, player_y)

def get_action(obs, player_x, player_y):
    """ get action of appropriate pattern in agent's memory """
    memory_patterns = find_patterns(obs, player_x, player_y)
    # find appropriate pattern in list of memory patterns
    for get_pattern in memory_patterns:
        pattern = get_pattern(obs, player_x, player_y)
        if pattern["environment_fits"](obs, player_x, player_y):
            return pattern["get_action"](obs, player_x, player_y)
    

# @human_readable_agent wrapper modifies raw observations 
# provided by the environment:
# https://github.com/google-research/football/blob/master/gfootball/doc/observation.md#raw-observations
# into a form easier to work with by humans.
# Following modifications are applied:
# - Action, PlayerRole and GameMode enums are introduced.
# - 'sticky_actions' are turned into a set of active actions (Action enum)
#    see usage example below.
# - 'game_mode' is turned into GameMode enum.
# - 'designated' field is removed, as it always equals to 'active'
#    when a single player is controlled on the team.
# - 'left_team_roles'/'right_team_roles' are turned into PlayerRole enums.
# - Action enum is to be returned by the agent function.
@human_readable_agent
def agent(obs):
    """ Ole ole ole ole """
    # dictionary for Memory Patterns data
    obs["memory_patterns"] = {}
    # coordinates of the ball in the next step
    obs["memory_patterns"]["ball_next_coords"] = {
        "x": obs["ball"][0] + obs["ball_direction"][0] * 2,
        "y": obs["ball"][1] + obs["ball_direction"][1] * 2
    }
    # Make sure player is running.
    if Action.Sprint not in obs["sticky_actions"]:
        return Action.Sprint
    # We always control left team (observations and actions
    # are mirrored appropriately by the environment).
    controlled_player_pos = obs["left_team"][obs["active"]]
    # get action of appropriate pattern in agent's memory
    action = get_action(obs, controlled_player_pos[0], controlled_player_pos[1])
    # return action
    return action
