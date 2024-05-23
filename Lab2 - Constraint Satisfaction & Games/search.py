from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    
    # Determine the current player's turn
    agent = game.get_turn(state)

    # Check if the current state is terminal
    terminal, values = game.is_terminal(state)
    
    # If terminal, return the values for all agents
    if terminal:
        return values[agent], None

    # If maximum depth is reached, evaluate the heuristic value for the current player's turn
    if max_depth == 0:
        # Player's turn (max node)
        if agent == 0:  
            return heuristic(game, state, agent), None
        
        # Monster's turn (min node)
        else:
            return -heuristic(game, state, agent), None  

    # Generate a list of possible actions and their resulting states
    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

    # If it's the player's turn (max node)
    if agent == 0:
        max_val = float('-inf')
        best_action = None
        # Iterate through possible actions and states
        for action, successor in actions_states:
            # Recursively call minimax for the successor state
            value, _ = minimax(game, successor, heuristic, max_depth - 1)
            # Update the maximum value and corresponding action
            if value > max_val:
                max_val = value
                best_action = action
        return max_val, best_action

    # If it's the monster's turn (min node)
    else:
        min_val = float('inf')
        best_action = None
        # Iterate through possible actions and states
        for action, successor in actions_states:
            # Recursively call minimax for the successor state
            value, _ = minimax(game, successor, heuristic, max_depth - 1)
            # Update the minimum value and corresponding action
            if value < min_val:
                min_val = value
                best_action = action
        return min_val, best_action
    


# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    # Get the turn of the player that starts the game
    turn = game.get_turn(state)

    def alphabeta_search(state, depth, alpha, beta):
        # Check if the state is terminal
        terminal, values = game.is_terminal(state)

        # If terminal, return the values for the original turn player
        if terminal:
            return values[turn], None

        # If depth reaches the maximum, return the heuristic value for the original turn player
        if depth == max_depth:
            return heuristic(game, state, turn), None

        # Get the current turn
        agent = game.get_turn(state)

        # If it is the turn of the player (MAX node)
        if agent == 0:
            # Generate a list of possible actions and their resulting states
            actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

            # Initialize the maximum value to negative infinity
            max_val = float('-inf')
            # Initialize the correct action to None
            best_action = None

            # Iterate through possible actions and states
            for action, successor in actions_states:
                # Recursively call the alphabeta_search function for the successor state
                successor_value, _ = alphabeta_search(successor, depth + 1, alpha, beta)

                # If the successor value is greater than the current maximum value, update the maximum value and correct action
                if successor_value > max_val:
                    max_val, best_action = successor_value, action

                # Prune the search if the maximum value is greater than or equal to beta
                if max_val >= beta:
                    return max_val, best_action

                # Update alpha to the maximum value
                alpha = max(alpha, max_val)

            # Return the maximum value and the correct action
            return max_val, best_action
        else:  # It is the turn of the enemy (MIN node)
            # Generate a list of possible actions and their resulting states
            actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

            # Initialize the minimum value to positive infinity
            min_val = float('inf')
            # Initialize the correct action to None
            best_action = None

            # Iterate through possible actions and states
            for action, successor in actions_states:
                # Recursively call the alphabeta_search function for the successor state
                successor_value, _ = alphabeta_search(successor, depth + 1, alpha, beta)

                # If the successor value is less than or equal to the current minimum value, update the minimum value and correct action
                if successor_value <= min_val:
                    min_val, best_action = successor_value, action

                # Prune the search if the minimum value is less than or equal to alpha
                if min_val <= alpha:
                    return min_val, best_action

                # Update beta to the minimum value
                beta = min(beta, min_val)

            # Return the minimum value and the correct action
            return min_val, best_action

    # Start the recursive search with initial depth, alpha, and beta
    _, best_action = alphabeta_search(state, 0, float('-inf'), float('inf'))
    # Return the best value and the best action
    return _, best_action




def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: float = float('-inf'), beta: float = float('inf')) -> Tuple[float, A]:
    # Get the turn of the player that starts the game
    turn = game.get_turn(state)

    def alphabeta_search_with_move_ordering(state, depth, alpha, beta):
        # Check if the state is terminal
        terminal, values = game.is_terminal(state)

        # If terminal, return the values for the original turn player
        if terminal:
            return values[turn], None

        # If depth reaches the maximum, return the heuristic value for the original turn player
        if depth == max_depth:
            return heuristic(game, state, turn), None

        # Get the current turn
        agent = game.get_turn(state)

        # If it is the turn of the player (MAX node)
        if agent == 0:
            # Generate a list of possible actions and their resulting states
            actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

            # Sort actions_states by heuristic value in descending order
            actions_states.sort(key=lambda x: heuristic(game, x[1], 0), reverse=True)

            # Initialize the maximum value to negative infinity
            max_val = float('-inf')
            # Initialize the correct action to None
            best_action = None

            # Iterate through possible actions and states
            for action, successor in actions_states:
                # Recursively call the alphabeta_search_with_move_ordering function for the successor value
                successor_value, _ = alphabeta_search_with_move_ordering(successor, depth + 1, alpha, beta)

                # If the successor value is greater than the current maximum value, update the maximum value and correct action
                if successor_value > max_val:
                    max_val, best_action = successor_value, action

                # Prune the search if the maximum value is greater than or equal to beta
                if max_val >= beta:
                    return max_val, best_action

                # Update alpha to the maximum value
                alpha = max(alpha, max_val)

            # Return the maximum value and the correct action
            return max_val, best_action
        else:  # It is the turn of the enemy (MIN node)
            # Generate a list of possible actions and their resulting states
            actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

            # Sort actions_states by heuristic value in ascending order
            actions_states.sort(key=lambda x: heuristic(game, x[1], 0))

            # Initialize the minimum value to positive infinity
            min_val = float('inf')
            # Initialize the correct action to None
            best_action = None

            # Iterate through possible actions and states
            for action, successor in actions_states:
                # Recursively call the alphabeta_search_with_move_ordering function for the successor value
                successor_value, _ = alphabeta_search_with_move_ordering(successor, depth + 1, alpha, beta)

                # If the successor value is less than or equal to the current minimum value, update the minimum value and correct action
                if successor_value <= min_val:
                    min_val, best_action = successor_value, action

                # Prune the search if the minimum value is less than or equal to alpha
                if min_val <= alpha:
                    return min_val, best_action

                # Update beta to the minimum value
                beta = min(beta, min_val)

            # Return the minimum value and the correct action
            return min_val, best_action

    # Start the recursive search with initial depth, alpha, and beta
    _, best_action = alphabeta_search_with_move_ordering(state, 0, float('-inf'), float('inf'))
    # Return the best value and the best action
    return _, best_action



# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    
    # Get the turn of the player that starts the game
    turn = game.get_turn(state)

    def recursive_expectimax(state, depth):
        # Check if the state is terminal
        terminal, values = game.is_terminal(state)
        
        # If the state is terminal, return the state utility
        if terminal:
            return values[turn], None

        # If the depth is equal to the maximum depth, return the heuristic value
        if depth == max_depth:
            return heuristic(game, state, turn), None

        # Get the current turn
        agent = game.get_turn(state)

        # Get the actions and the successors of the state
        actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]

        # If the current turn is 0, return the maximum value of the successors
        if agent == 0:
                    
            # Initialize the maximum value to negative infinity
            max_val = float('-inf')

            # Initialize the correct action to None
            best_action = None

            # Loop through the actions and the successors
            for action, state in actions_states:
                # Get the value of the successor
                successor_value = recursive_expectimax(state, depth + 1)[0]

                # If the successor value is greater than the maximum value, update the maximum value and correct action
                if successor_value > max_val:
                    max_val, best_action = successor_value, action

            # Return the maximum value and the correct action
            return max_val, best_action

        # If the current turn is not 0, return the expected value of the successors
        else:

            # Initialize the expected value to 0
            expected_val = 0

            # Loop through the actions and the successors
            for _, state in actions_states:
                # Get the value of the successor
                successor_value = recursive_expectimax(state, depth + 1)[0]

                # Update the expected value by adding the successor value to the expected value
                expected_val += successor_value

            # Return the expected value and the correct action
            return expected_val / len(actions_states), None

    return recursive_expectimax(state, 0)
