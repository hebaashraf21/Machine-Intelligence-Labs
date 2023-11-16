from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented


#TODO: Import any modules you want to use
import heapq



# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE

    # Given the following pseudo code from the reference:
    '''
        node ←a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
        if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        frontier ← a FIFO queue with node as the only element
        explored ← an empty set
        loop do
        if EMPTY?(frontier ) then return failure
        node ← POP(frontier ) /* chooses the shallowest node in frontier */
        add node.STATE to explored
        for each action in problem.ACTIONS(node.STATE) do
        child ← CHILD-NODE(problem, node, action)
        if child.STATE is not in explored or frontier then
        if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
        frontier ← INSERT(child,frontier )
    '''
    # Check if the root is already the goal state
    if problem.is_goal(initial_state):
        return []
    
    # Initialize the root node with the initial state
    node = initial_state

    # Initialize a FIFO queue (frontier) for node expansion
    '''
    Why using a queue: to ensures exploration of shallower nodes first.
                       BFS explores nodes in the order they were added to the frontier.
                       This means that it explores all nodes at a given depth level before moving on to nodes at the next depth level. 
    '''
    frontier = deque()

    # Add the root to the frontier along with its path 
    frontier.append((node, []))  

    # Initialize a set to keep track of explored states
    explored = set()

    while frontier:
        # Pop the shallowest node from the frontier along with its path
        node, path = frontier.popleft()

        # Skip nodes that have already been explored
        if node in explored:
            continue

        # Mark the node as explored
        explored.add(node)

        # Explore possible actions from the current node
        for action in problem.get_actions(node):
            # Generate the child node resulting from the action
            child = problem.get_successor(node, action)

            # Ensure the child is not already in explored or frontier
            if child not in explored and child not in frontier:

                # Extend the path with the current action
                new_path = path + [action]
                # If the child is the goal state, return the path
                if problem.is_goal(child):
                    return new_path

                 # Add the child node and its extended path to the frontier
                frontier.append((child, new_path))

    # If no solution is found, return None
    return None          



def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE

    # Check if the root is already the goal state
    if problem.is_goal(initial_state):
        return []

    # Initialize the root node with the initial state
    node = initial_state
    
    # Initialize a stack (frontier) for node expansion
    '''
    Why using a stack: to mimic the recursive nature of DFS.
    '''
    frontier = []

    # Add the root to the frontier along with an empty path
    frontier.append((node, []))  # <== Last in

    # Initialize a set to keep track of explored states
    explored = set()

    while frontier:
        # Pop the deepest node from the frontier
        node, path = frontier.pop() # ==> First out

        # Skip nodes that have already been explored
        if node in explored:
            continue

        # Mark the node as explored
        explored.add(node)

        # If the node is the goal state, return the path
        if problem.is_goal(node):
            return path

        # Explore possible actions from the current node
        for action in problem.get_actions(node):
            # Generate the child node resulting from the action
            child = problem.get_successor(node, action)

            # Ensure the child is not already in explored or frontier
            if child not in explored and child not in frontier:

                # Add the child node and extend the path
                frontier.append((child, path + [action]))

    # If no solution is found, return None
    return None    
    

def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # Given the following pseudo code from the reference:
    '''
        function UNIFORM-COST-SEARCH(problem) returns a solution, or failure
        node ←a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
        frontier ← a priority queue ordered by PATH-COST, with node as the only element
        explored ← an empty set
        loop do
        if EMPTY?(frontier ) then return failure
        node ← POP(frontier ) /* chooses the lowest-cost node in frontier */
        if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        add node.STATE to explored
        for each action in problem.ACTIONS(node.STATE) do
        child ← CHILD-NODE(problem, node, action)
        if child.STATE is not in explored or frontier then
        frontier ← INSERT(child,frontier )
        else if child.STATE is in frontier with higher PATH-COST then
        replace that frontier node with child
    ''' 

    # Check if the root is already the goal state
    if problem.is_goal(initial_state):
        return []
    
    # Initialize the root node with the initial state
    node = initial_state   

    # Using a dictionary (hash table) for the frontier:
    # - Key: states to be expanded
    # - Value: tuple with (path cost, list of actions)
    frontier ={node: (0, [])}

    # Initialize a set to keep track of explored states
    explored = set()

    while frontier:
        # Get the node to be expanded (the one with the lowest path cost)
        node = min(frontier, key=lambda k: frontier[k][0])
        cost, actions = frontier[node]

        # Remove the node from the frontier
        frontier.pop(node)

        # Mark the node as explored
        explored.add(node)

        # If the node is the goal state, return the path
        if problem.is_goal(node):
            return actions

        # Loop over all the possible actions of the current state
        for action in problem.get_actions(node):
            # Evaluate the action cost
            action_cost = cost + problem.get_cost(node, action)

            child_node = problem.get_successor(node, action)

            # Check if the child node is not in the frontier and also not in the explored set
            # to prevent expansion of the same node more than one time
            # Or the node exists in the frontier with a larger path cost
            if (child_node not in frontier and child_node not in explored) \
                    or (child_node in frontier and action_cost < frontier[child_node][0]):
                # Add/update the child node in the frontier with its path cost and actions
                frontier[child_node] = (action_cost, actions + [action])

    # Return None if no solution is found
    return None



def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
    # Check if the root is already the goal state
    if problem.is_goal(initial_state):
        return []

    # Initialize the root node with the initial state
    node = initial_state

    # Using a dictionary for the frontier:
    # Key: node, Value: tuple (total_cost + heuristic, actions)
    frontier = {node: (0 + heuristic(problem, node), [])}

    # Initialize a set to keep track of explored states
    explored = set()

    while frontier:
        # Get the node with the highest priority (lowest total cost)
        node = min(frontier, key=lambda k: frontier[k][0])
        total_cost, actions = frontier.pop(node)

        # If the node is the goal state, return the path
        if problem.is_goal(node):
            return actions

        # Mark the node as explored
        explored.add(node)

        # Loop over all the possible actions of the current state
        for action in problem.get_actions(node):
            child_node = problem.get_successor(node, action)
            action_cost = problem.get_cost(node, action)

            # Check if the child_node is in the frontier
            in_frontier = child_node in frontier

            # If the child_node is neither in the frontier nor explored, or it's in the frontier with a higher cost
            if child_node not in explored and not in_frontier:
                new_path = actions + [action]
                new_total_cost = total_cost - heuristic(problem, node) + action_cost + heuristic(problem, child_node)
                frontier[child_node] = (new_total_cost, new_path)
            elif in_frontier:
                # Check if the new path is better (lower cost)
                frontier_cost = frontier[child_node][0]
                new_path_cost = total_cost - heuristic(problem, node) + action_cost + heuristic(problem, child_node)
                if new_path_cost < frontier_cost:
                    # Update the frontier with the lower cost path
                    frontier[child_node] = (new_path_cost, actions + [action])

    # Return None if no solution is found
    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    #TODO: ADD YOUR CODE HERE
     # Check if the root is already the goal state
    if problem.is_goal(initial_state):
        return []
    
    # Initialize the root node with the initial state
    node = initial_state

    # Using a dictionary (hash table) for the frontier:
    # - Key: states to be expanded
    # - Value: tuple with (heuristic value, list of actions)
    frontier ={node: (heuristic(problem, node), [])}

    # Initialize a set to keep track of explored states
    explored = set()

    while frontier:
        # Get the node with the highest priority (lowest heuristic value)
        node = min(frontier, key=lambda k: frontier[k][0])
        _, actions = frontier[node]

        # Remove the node from the frontier
        frontier.pop(node)

        # If the node is the goal state, return the path
        if problem.is_goal(node):
            return actions

        # Mark the node as explored
        explored.add(node)

        # Loop over all the possible actions of the current state
        for action in problem.get_actions(node):
            child_node = problem.get_successor(node, action)

            if child_node not in frontier and child_node not in explored:
                new_path = actions + [action]
                frontier[child_node] = (heuristic(problem, child_node), new_path)

    # Return None if no solution is found
    return None






