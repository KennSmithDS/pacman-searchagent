# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
import traceback
import sys

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    try:
        try:
            problemType = problem.problemType
            # print(f'Attempting to solve {problemType} with Breadth First Search algorithm')
        except AttributeError:
            # print('Problem test case does not have problem type attribute!')
            problemType = 'SearchProblem'
            pass

        # calling the starting state for the assigned problem class
        startingState = problem.getStartState()
        # print('This is the starting position (x,y): ', startingState)

        # iterative attempt at DFS
        def dfsGraphSearchv2(start):
            explored = set()
            frontier = util.Stack()
            frontier.push((start, ['Start']))

            while not frontier.isEmpty():
                whereAmI, currentPath = frontier.pop()
                if problem.isGoalState(whereAmI):
                    return currentPath[1:]

                if whereAmI not in explored:
                    explored.add(whereAmI)
                    
                nextMoves = problem.getSuccessors(whereAmI)
                for move in nextMoves:
                    # this is where the extra expanded notes are coming from for problem 1
                    if move[0] not in explored and not frontier.inStack(move[0]):
                        # explored.add(move[0])
                        frontier.push((move[0], currentPath + [move[1]]))

        result = dfsGraphSearchv2(startingState)
        print('-'*80)
        print(result)
        print('-'*80)
        return result

    except Exception as e:
        print('-'*80)
        print(f'Error {e} found in code: ', traceback.print_exc(file=sys.stdout))
        print('-'*80)

    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    try:
        try:
            problemType = problem.problemType
            print(f'Attempting to solve {problemType} with Breadth First Search algorithm')
        except AttributeError:
            print('Problem test case does not have problem type attribute!')
            problemType = 'SearchProblem'
            pass

        # second attempt at iterative BFS that seems to follow algorithm logic best
        def bfsGraphSearch(start):
            explored = set()
            frontier = util.Queue()
            # tupleHolder = tuple((0,0))
            directionHolder = ['Start']
            frontier.push([start, directionHolder])
            # print(frontier.list)

            while not frontier.isEmpty():
                whereAmI, currentPath = frontier.pop()
                # print(f'Currently standing on {whereAmI}')
                # print(f'This is how pac-man got here: {currentPath}')

                if problem.isGoalState(whereAmI):
                    return currentPath[1:], whereAmI
                else:
                    if whereAmI not in explored:
                        # print(f'Adding {whereAmI} to explored and adding successors to frontier')
                        explored.add(whereAmI)
                        nextMoves = problem.getSuccessors(whereAmI)
                        # print('Successive moves possible ', nextMoves)

                        # if len(nextMoves) > 1:
                        for move in nextMoves:
                            if move[0] not in explored and not frontier.inQueue(move[0]):
                                frontier.push([move[0], currentPath + [move[1]]])

        initialState = problem.getStartState()
        print('This is the starting position (x,y): ', initialState)

        # directionSequence, goalState = bfsGraphSearch(initialState)

        # this calls the problem attribute problemType to check if solving corners problem or not

        if problemType == 'CornersProblem':
                                    
            enterState = initialState
            cornerStates = problem.corners
            statePairs = {}
            directionTable = util.PriorityQueue()
            problem.cornersVisited = set()

            for corner in cornerStates:
                # print(f'{corner} is the first target corner out of {problem.numCorners}')
                problem.firstTargetReached = False
                problem.setNextTarget(corner)
                directionsFromStartStateQueue = util.Queue()
                    
                while len(problem.cornersVisited) < problem.numCorners:
                    # print(f'{len(problem.cornersVisited)} corners have been visited')
                    path, exitState = bfsGraphSearch(enterState)
                    # print(f'Path found from {enterState} to {exitState}:\n', path)
                    directionsFromStartStateQueue.push(path)
                    problem.cornersVisited.add(exitState)
                    enterState = exitState
                    
                directionAccumulator = []
                while not directionsFromStartStateQueue.isEmpty():
                    directionAccumulator.extend(directionsFromStartStateQueue.pop())
                statePairs[(initialState, corner)] = [directionAccumulator, len(directionAccumulator)]

            for value in statePairs.values():
                if value[0]:
                    directionTable.push((value[0]), value[1])
            directionSequence = directionTable.pop()

        else:
            directionSequence, goalState = bfsGraphSearch(initialState)
            
        print('-'*80)
        print(directionSequence)
        print('-'*80)
        return directionSequence

    except Exception as e:
        print('-'*80)
        print(f'Error {e} found in code: ', traceback.print_exc(file=sys.stdout))
        print('-'*80)

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    try:
        try:
            problemType = problem.problemType
            # print(f'Attempting to solve {problemType} with Breadth First Search algorithm')
        except AttributeError:
            # print('Problem test case does not have problem type attribute!')
            problemType = 'SearchProblem'
            pass

        def ucsGraphSearch(start):
            explored = set()
            frontier = util.PriorityQueue()
            frontier.push((start, []), 0)

            while not frontier.isEmpty():
                whereAmI, currentPath = frontier.pop()

                if problem.isGoalState(whereAmI):
                    return currentPath

                if whereAmI not in explored:
                    explored.add(whereAmI)
                    nextMoves = problem.getSuccessors(whereAmI)
                    for move in nextMoves:
                        if move[0] not in explored and not frontier.inHeap(move[0]):
                            nextStep = move[1]
                            stepsTaken = currentPath + [nextStep]
                            costToGetHere = problem.getCostOfActions(stepsTaken)
                            frontier.push((move[0], currentPath + [move[1]]), costToGetHere)

        # initializing an empty set to store all explored nodes and adding default start state
        initialState = problem.getStartState()
        print('This is the starting position (x,y): ', initialState)

        result = ucsGraphSearch(initialState)
        print('-'*80)
        print(result)
        print('-'*80)
        return result

    except Exception as e:
        print('-'*80)
        print(f'Error {e} found in code: ', traceback.print_exc(file=sys.stdout))
        print('-'*80)

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    try:
        try:
            problemType = problem.problemType
            # print(f'Attempting to solve {problemType} with Breadth First Search algorithm')
        except AttributeError:
            # print('Problem test case does not have problem type attribute!')
            problemType = 'SearchProblem'
            pass

        def aStarGraphSearch(start):
            explored = set()
            frontier = util.PriorityQueue()
            frontier.push((start, []), 0)
            # print(frontier)

            while not frontier.isEmpty():
                whereAmI, currentPath = frontier.pop()
                # print(f'Currently standing on {whereAmI}')
                # print(f'This is how pac-man got here: {currentPath}')

                if problem.isGoalState(whereAmI):
                    return currentPath, whereAmI
                if whereAmI not in explored:
                    explored.add(whereAmI)
                    nextMoves = problem.getSuccessors(whereAmI)
                    for move in nextMoves:
                        # print(f'Visiting: {move}')
                        if move[0] not in explored:
                            nextState = move[0]
                            nextStep = move[1]
                            stepsTaken = currentPath + [nextStep]
                            costToGetHere = problem.getCostOfActions(stepsTaken)
                            costToGetToGoal = heuristic(nextState, problem)
                            # print(f'Cost of heuristic at {move[0]} is {costToGetToGoal}')
                            totalFnCost = costToGetHere + costToGetToGoal
                            frontier.push((move[0], currentPath + [move[1]]), totalFnCost)

        initialState = problem.getStartState()
        print('This is the starting position (x,y): ', initialState)
        # directionSequence, goalState = aStarGraphSearch(initialState)

        if problemType == 'CornersProblem':
                                    
            enterState = initialState
            cornerStates = problem.corners
            statePairs = {}
            directionTable = util.PriorityQueue()
            problem.cornersVisited = set()

            for corner in cornerStates:
                # print(f'{corner} is the first target corner out of {problem.numCorners}')
                # problem.cornersVisited = set()
                problem.firstTargetReached = False
                problem.setNextTarget(corner)
                # problem.cornerTarget = corner
                # print(f'{problem.cornerTarget} is now the target corner')
                directionsFromStartStateQueue = util.Queue()
                    
                while len(problem.cornersVisited) < problem.numCorners:
                    # print(f'{len(problem.cornersVisited)} corners have been visited')
                    path, exitState = aStarGraphSearch(enterState)
                    # print(f'Path found from {enterState} to {exitState}:\n', path)
                    directionsFromStartStateQueue.push(path)
                    problem.cornersVisited.add(exitState)
                    enterState = exitState
                    
                directionAccumulator = []
                while not directionsFromStartStateQueue.isEmpty():
                    directionAccumulator.extend(directionsFromStartStateQueue.pop())
                statePairs[(initialState, corner)] = [directionAccumulator, len(directionAccumulator)]

            for value in statePairs.values():
                if value[0]:
                    directionTable.push((value[0]), value[1])
            directionSequence = directionTable.pop()

        else:
            directionSequence, goalState = aStarGraphSearch(initialState)
            
        print('-'*80)
        print(directionSequence)
        print('-'*80)
        return directionSequence

    except Exception as e:
        print('-'*80)
        print(f'Error {e} found in code: ', traceback.print_exc(file=sys.stdout))
        print('-'*80)

    util.raiseNotDefined()

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
