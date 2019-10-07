# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
        prevGameState = currentGameState
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = currentGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        minVal = float('inf')
        oldPos = currentGameState.getPacmanPosition()
        for coord in newFood:
          if minVal > util.manhattanDistance(newPos,coord):
            minVal = util.manhattanDistance(newPos,coord)
        minEnemy = float('inf')
        for state in newGhostStates:
          if minEnemy > util.manhattanDistance(newPos,state.getPosition()):
            minEnemy = util.manhattanDistance(newPos,state.getPosition())
        if minEnemy < 2:
          minVal = 99999999
        if successorGameState.getPacmanPosition()  == prevGameState.getPacmanPosition():
          minVal += 9999999
        if minVal == float('inf'):
          return float('inf')
        return successorGameState.getScore() - minVal  + 1

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
        "*** YOUR CODE HERE ***"
        
        def getmax(state, depth, agentIndex):
          actions = state.getLegalActions(0)
          if not actions or depth ==0 or state.isWin():
            return self.evaluationFunction(state), Directions.STOP
          maxVal = float('-inf')
          bestAction = Directions.STOP
          for action in actions:
            successor = state.generateSuccessor(0,action)
            temp = getmin(successor, depth, 1)
            if temp > maxVal:
              maxVal = temp
              bestAction = action
          return (maxVal, bestAction)

        def getmin(state, depth, agentIndex):
          actions = state.getLegalActions(agentIndex)
          if not actions or depth ==0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          minVal = float('inf')
          if agentIndex == state.getNumAgents() -1:
            for action in actions:
              successor = state.generateSuccessor(agentIndex,action)
              minVal = min(minVal, getmax(successor, depth -1, 0)[0])
          else:
            for action in actions:
              successor = state.generateSuccessor(agentIndex,action)
              minVal = min(minVal, getmin(successor, depth, agentIndex +1))
          return minVal


        return getmax(gameState, self.depth, 0)[1]

        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def getmax(state, depth, agentIndex, a, b):
          actions = state.getLegalActions(0)
          if not actions or depth ==0 or state.isWin():
            return self.evaluationFunction(state), Directions.STOP
          maxVal = float('-inf')
          bestAction = Directions.STOP
          for action in actions:
            successor = state.generateSuccessor(0,action)
            temp = getmin(successor, depth, 1, a, b)
            if temp > maxVal:
              maxVal = temp
              bestAction = action
            if maxVal > b:
              return maxVal, bestAction
            a = max(a, maxVal)
          return (maxVal, bestAction)

        def getmin(state, depth, agentIndex, a, b):
          actions = state.getLegalActions(agentIndex)
          if not actions or depth ==0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          minVal = float('inf')
          if agentIndex == state.getNumAgents() -1:
            for action in actions:
              successor = state.generateSuccessor(agentIndex,action)
              minVal = min(minVal, getmax(successor, depth -1, 0, a, b)[0])
              if minVal < a:
                return minVal
              b = min(b, minVal)
          else:
            for action in actions:
              successor = state.generateSuccessor(agentIndex,action)
              minVal = min(minVal, getmin(successor, depth, agentIndex +1, a, b))
              if minVal < a:
                return minVal
              b = min(b, minVal)
          return minVal

        a = float('-inf')
        b = float('inf')
        return getmax(gameState, self.depth, 0, a, b)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        def getmax(state, depth, agentIndex):
          actions = state.getLegalActions(0)
          if not actions or depth ==0 or state.isWin():
            return self.evaluationFunction(state), Directions.STOP
          maxVal = float('-inf')
          bestAction = Directions.STOP
          for action in actions:
            successor = state.generateSuccessor(0,action)
            temp = getexp(successor, depth, 1)
            if temp > maxVal:
              maxVal = temp
              bestAction = action
          return (maxVal, bestAction)

        def getexp(state, depth, agentIndex):
          actions = state.getLegalActions(agentIndex)
          if not actions or depth ==0 or state.isWin() or state.isLose():
            return self.evaluationFunction(state)
          vals = []
          if agentIndex == state.getNumAgents() -1:
            for action in actions:
              successor = state.generateSuccessor(agentIndex,action)
              vals.append(getmax(successor, depth -1, 0)[0])
          else:
            for action in actions:
              successor = state.generateSuccessor(agentIndex,action)
              vals.append(getexp(successor, depth, agentIndex +1))
          return sum(vals)/len(vals)


        return getmax(gameState, self.depth, 0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    minEnemy = float('inf')
    totalDist = 0
    newPos = pos[:]
    tempPos = pos[:]
    foodList = food[:]
    powerUps = currentGameState.getCapsules()
    minVal = 0
    while len(foodList) > 0: #gets total distance between pacman and getting every food item
      minVal = float('inf')
      for coord in foodList:
        if minVal > util.manhattanDistance(newPos,coord):
          minVal = util.manhattanDistance(newPos,coord)
          tempPos = coord[:]
      foodList.remove(tempPos)
      newPos = tempPos[:]
      totalDist += minVal

    for state in ghostStates: #gets distance to closest ghost
      if minEnemy > util.manhattanDistance(pos,state.getPosition()):
        minEnemy = util.manhattanDistance(pos,state.getPosition())
    newPos = pos[:]
    tempPos = pos[:]
    totalPower = 0
    while len(powerUps) > 0:
      minPowerUp = float('inf')
      for coord in currentGameState.getCapsules(): #gets distance to closest powerup
        if minPowerUp > util.manhattanDistance(newPos,coord):
          minPowerUp = util.manhattanDistance(newPos,coord)
          tempPos = coord[:]
      powerUps.remove(tempPos)
      newPos = tempPos[:]
      totalPower += minPowerUp

    if minEnemy < 2:
      minVal = 9999
    rand = random.randint(0,1)
    rand2 = random.randint(0,1)
    rand3 = random.randint(0,1)
    rand = rand * rand2 * rand3
    
    return currentGameState.getScore() - totalDist - minVal + rand - totalPower * 5

# Abbreviation
better = betterEvaluationFunction

