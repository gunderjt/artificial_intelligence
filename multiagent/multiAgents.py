# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        ghostWeight = 1
        foodWeight = 4.0
        scoreWeight = 1.0
        # weight (4) * distance to nearest food pellet - 
        # weight(10) * distance to nearest ghost.
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        pelletDist = 999999999.0
        ghostDist = 999999999.0
        for foodPellet in newFood:
            dist = util.manhattanDistance(newPos, foodPellet)
            if dist < pelletDist:
                pelletDist = dist
        newGhost = successorGameState.getGhostPositions()
        for ghost in newGhost:
            dist = util.manhattanDistance(newPos, ghost)
            if dist < ghostDist:
                ghostDist = dist
                if ((dist == 1) or (dist == 0)):
                    return -999999999999
#            if ghostDist > 8:
#                ghostDist = 0
        score = successorGameState.getScore()
#       print (foodWeight*(1/float(pelletDist))) + (scoreWeight*score)
        return (foodWeight*(1/float(pelletDist))) + (scoreWeight*score)
#        newGhostStates = successorGameState.getGhostStates()
#        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """
    def max_value(self, state, agent, maxAgents, depth, maxDepth):
        if depth > maxDepth or state.isWin() or state.isLose():
            return [self.evaluationFunction(state), "none"]
        depth += 1
        v = -9999999999999
        legalAction = state.getLegalActions(agent)
#        print "max_value: ", len(legalAction)
        bestAction = ""
        for action in legalAction:
            actionV = self.min_value(state.generateSuccessor(agent, action), agent+1, maxAgents, depth, maxDepth)
#            print "max_value: ", actionV[0]
            if actionV[0] > v:
                v = actionV[0]
                bestAction = action
        return [v, bestAction]

    def min_value(self, state, agent, maxAgents, depth, maxDepth):
        if state.isWin() or state.isLose():
            return [self.evaluationFunction(state), "none"]
        legalAction = state.getLegalActions(agent)
#        print "min_value: ", len(legalAction)
#            print "Getting called"
        bestAction = ""
        if (agent < (maxAgents-1)):
            v = 999999999999
            for action in legalAction:
                actionV = self.min_value(state.generateSuccessor(agent, action), agent+1, maxAgents, depth, maxDepth)
                if actionV[0] < v:
                    v = actionV[0]
                    bestAction = action
            return [v, bestAction]
        else:
            v = 99999999999
            for action in legalAction:
                actionV = self.max_value(state.generateSuccessor(agent, action), 0, maxAgents, depth, maxDepth)
                if actionV[0] < v:
                    v = actionV[0]
                    bestAction = action
            return [v, bestAction]

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
#        print self.max_value(gameState, 0, gameState.getNumAgents(), 1, self.depth)[0]
        return self.max_value(gameState, 0, gameState.getNumAgents(), 1, self.depth)[1]
        
        util.raiseNotDefined()
    





class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def max_value(self, state, agent, maxAgents, depth, maxDepth, alpha, beta):
        if depth > maxDepth or state.isWin() or state.isLose():
            return [self.evaluationFunction(state), "none"]
        depth += 1
        v = -9999999999999
        legalAction = state.getLegalActions(agent)
#        print "max_value: ", len(legalAction)
        bestAction = ""
        for action in legalAction:
            actionV = self.min_value(state.generateSuccessor(agent, action), agent+1, maxAgents, depth, maxDepth, alpha, beta)
            if actionV[0] > v:
                v = actionV[0]
                bestAction = action
            if v > beta:
                return [v, "none"]
            alpha = max(alpha, actionV[0])
        return [v, bestAction]

    def min_value(self, state, agent, maxAgents, depth, maxDepth, alpha, beta):
        if state.isWin() or state.isLose():
            return [self.evaluationFunction(state), "none"]
        legalAction = state.getLegalActions(agent)
#        print "min_value: ", len(legalAction)
#            print "Getting called"
        bestAction = ""
        if (agent < (maxAgents-1)):
            v = 999999999999
            for action in legalAction:
                actionV = self.min_value(state.generateSuccessor(agent, action), agent+1, maxAgents, depth, maxDepth, alpha, beta)
                if actionV[0] < v:
                    v = actionV[0]
                    bestAction = action
                if v < alpha:
                    return [v, "none"]
                beta = min(beta, actionV[0])
            return [v, bestAction]
        else:
            v = 99999999999
            for action in legalAction:
                actionV = self.max_value(state.generateSuccessor(agent, action), 0, maxAgents, depth, maxDepth, alpha, beta)
                if actionV[0] < v:
                    v = actionV[0]
                    bestAction = action
                if v < alpha:
                    return [v, "none"]
                beta = min(beta, actionV[0])
            return [v, bestAction]


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.max_value(gameState, 0, gameState.getNumAgents(), 1, self.depth, -999999999, 9999999999)[1]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def pacman_value(self, state, agent, maxAgents, depth, maxDepth):
        if depth > maxDepth or state.isWin() or state.isLose():
            return [self.evaluationFunction(state), "none"]
        depth += 1
        v = -9999999999999
        legalAction = state.getLegalActions(agent)
#        print "max_value: ", len(legalAction)
        bestAction = ""
        for action in legalAction:
            actionV = self.ghost_value(state.generateSuccessor(agent, action), agent+1, maxAgents, depth, maxDepth)
#            print "max_value: ", actionV[0]
            if actionV[0] > v:
                v = actionV[0]
                bestAction = action
        return [v, bestAction]

    def ghost_value(self, state, agent, maxAgents, depth, maxDepth):
        if state.isWin() or state.isLose():
            return [self.evaluationFunction(state), "none"]
        legalAction = state.getLegalActions(agent)
#        print "min_value: ", len(legalAction)
#            print "Getting called"
        bestAction = ""
        if (agent < (maxAgents-1)):
            v = 0
            for action in legalAction:
                actionV = self.ghost_value(state.generateSuccessor(agent, action), agent+1, maxAgents, depth, maxDepth)
                v += actionV[0]
            v = float(v)/len(legalAction)
            return [v, "none"]
        else:
            v = 0
            for action in legalAction:
                actionV = self.pacman_value(state.generateSuccessor(agent, action), 0, maxAgents, depth, maxDepth)
                v += actionV[0]
            v = float(v)/len(legalAction)
            return [v, "none"]

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.pacman_value(gameState, 0, gameState.getNumAgents(), 1, self.depth)[1]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    if currentGameState.isLose():
        return -99999999999999999
    ghostWeight, foodWeight, scoreWeight, capsuleWeight = 0.001, 4.0, 200000.0, 0.0
    # weight (4) * distance to nearest food pellet - 
    # weight(10) * distance to nearest ghost.
    foodScore, ghostScore, scoreScore, capsuleScore = 0.0, 0.0, 0.0, 0.0
    newPos = currentGameState.getPacmanPosition()



    #get food score, how much does pacman want to eat go into the weight
    newFood = currentGameState.getFood().asList()
    pelletDist = 999999999.0
    pelletTotal = 0.0
    for foodPellet in newFood:
        dist = util.manhattanDistance(newPos, foodPellet)
        pelletTotal += dist
        if dist < pelletDist:
            pelletDist = dist
    foodScore = (foodWeight*(1/float(pelletDist))) + 1/(pelletTotal+1)

    #get ghost score, how afraid/attracted to the ghost is pacman
    ghostDist = 999999999.0
    newGhost = currentGameState.getGhostPositions()
    ghostState = currentGameState.getGhostStates()
    scareTime = 0
    for ghost in ghostState:
        scareTime += ghost.scaredTimer
    for ghost in newGhost:
        dist = util.manhattanDistance(newPos, ghost)
        if dist < ghostDist:
            ghostDist = dist
            if (dist < 2) and (scareTime == 0):
                return -999999999999
    ghostScore = ghostDist*ghostWeight*-1
    if scareTime > 0:
        ghostScore *= -1
    #get capsule score, if a capsule and a ghost are nearby, eat capsule kill ghost
    newCapsule = currentGameState.getCapsules()
    capsuleDist = 999999999999.0
    for capsule in newCapsule:
        dist = util.manhattanDistance(newPos, capsule)
        if dist < capsuleDist:
            capsuleDist = dist
            if capsuleDist < 3 and ghostDist < 6:
                capsuleWeight = 200
    capsuleScore = capsuleWeight*(1/float(capsuleDist))
    score = foodScore + (scoreWeight*currentGameState.getScore()) + ghostScore + capsuleScore 
    return score


# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
    """
      Your agent for the mini-contest
    """

    def getAction(self, gameState):
        """
          Returns an action.  You can use any method you want and search to any depth you want.
          Just remember that the mini-contest is timed, so you have to trade off speed and computation.

          Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
          just make a beeline straight towards Pacman (or away from him if they're scared!)
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

