# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        # Write value iteration code here
        
        states = self.mdp.getStates()
        #need temporary storage of state values, then after they are all incremented, update values[state]
        incValues = util.Counter()
        for i in range(self.iterations):
            for state in states:
                actions = self.mdp.getPossibleActions(state)
                alpha = -9999999999999999
                for action in actions:
                    qValue = self.getQValue(state, action)
                    alpha = max(alpha, qValue)
                if alpha != -9999999999999999:
                    incValues[state] = alpha
               # print "temp action", action
               # print "temp value" incValues[state]
            #update self.values[state]
            for state in states:
                self.values[state] = incValues[state]
                #print "state", state

    def initCounter(self, counter, states):
        for state in states:
            counter[state] = -99999999999
        return counter
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        sumation = 0
        transitions = self.mdp.getTransitionStatesAndProbs(state, action)
        # p transitions[0]
        for transition in transitions:
            reward = self.mdp.getReward(state, action, transition[0])
            itValue = self.getValue(transition[0])
            sumation += transition[1]*(reward + self.discount*itValue)
        #print action
        #print sumation
        return sumation
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        calcActions = util.Counter()
        actions = self.mdp.getPossibleActions(state)
        for action in actions:
            calcActions[action] = self.getQValue(state, action)
            #p calcActions[action]
        return calcActions.argMax()
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
