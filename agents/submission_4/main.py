import sys
sys.path.append("/agents/")

import numpy as np
from kaggle_environments.envs.football.helpers import *
from scenarios import corner, penalty, freekick, normal, throwin, kickoff
from consts import *

class agentLogic:
	def __init__(self, obs):
		self.obs = obs
	
	def isPenalty(self):
		return self.obs["game_mode"] == GameMode.Penalty
	
	def isCorner(self):
		return self.obs["game_mode"] == GameMode.Corner

	def isFreeKick(self):
		return self.obs["game_mode"] == GameMode.FreeKick
	
	def isKickOff(self):
		return self.obs["game_mode"] == GameMode.KickOff

	def isGoalKick(self):
		return self.obs["game_mode"] == GameMode.GoalKick

	def isThrowIn(self):
		return self.obs["game_mode"] == GameMode.ThrowIn

	def makeAction(self):
		"""
		Return the agent's desire action
		"""
		if self.isPenalty():
			return penalty.Penalty(self.obs).makePenaltyAction()

		if self.isCorner():
			return corner.Corner(self.obs).makeCornerAction()
		
		if self.isFreeKick():
			return freekick.FreeKick(self.obs).makeFreeKickAction()
		
		if self.isThrowIn():
			return throwin.ThrowIn(self.obs).makeThrowInAction()
		
		if self.isKickOff():
			return kickoff.KickOff(self.obs).makeKickOffAction()
		
		logic = normal.Normal(self.obs)
		return logic.makeAction()

@human_readable_agent
def agent(obs):
	myAgent = agentLogic(obs)
	return myAgent.makeAction()