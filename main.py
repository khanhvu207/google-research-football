import sys
sys.path.append("/kaggle_simulations/agent")

from consts import *
from game_modes import *
from kaggle_environments.envs.football.helpers import *

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
			return Penalty(self.obs).makePenaltyAction()

		if self.isCorner():
			return Corner(self.obs).makeCornerAction()
		
		if self.isFreeKick():
			return FreeKick(self.obs).makeFreeKickAction()
		
		if self.isThrowIn():
			return ThrowIn(self.obs).makeThrowInAction()
		
		if self.isKickOff():
			return KickOff(self.obs).makeKickOffAction()

		logic = Normal(self.obs)
		return logic.makeAction()

@human_readable_agent
def agent(obs):
	myAgent = agentLogic(obs)
	return myAgent.makeAction()