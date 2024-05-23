from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        # Check if the current state is terminal
        if self.mdp.is_terminal(state):
            return 0  


        # Define a function to calculate the Bellman equation for a specific action
        def calculate_bellman_equation(action):
            # Find next states (successors) based on the action
            successors = self.mdp.get_successor(state, action)

            # Initialize the sum to zero
            utility_sum = 0

            # Perform the Bellman equation on the successors
            for successor in successors:
                # Get the reward for the current state, action, and successor
                reward = self.mdp.get_reward(state, action, successor)
                
                # Calculate the discounted utility for the successor
                discounted_utility = self.discount_factor * self.utilities[successor]

                # Update the utility sum using the Bellman equation
                utility_sum += successors[successor] * (reward + discounted_utility)

            return utility_sum
        
        # Find all possible actions based on the current state
        actions = self.mdp.get_actions(state)

        # Create a temporary array to store utilities to choose the max utility after this step
        results = []

        # Iterate over all actions to calculate utilities
        for action in actions:
            # Calculate utility using the defined function
            utility_sum = calculate_bellman_equation(action)
            
            # Store the calculated utility in the temporary array
            results.append(utility_sum)

        # Return the max utility among all calculated utilities
        return max(results)

    


    
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function

        # Calculate utility changes for each state
        utility_changes = [abs(self.compute_bellman(state) - self.utilities[state]) for state in self.mdp.get_states()]

        # Update the utilities with the newly computed values
        self.utilities = {state: self.compute_bellman(state) for state in self.mdp.get_states()}

        # Check if all utility changes are within the specified tolerance
        return all(change <= tolerance for change in utility_changes)


    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        iteration = 0  # Initialize the iteration counter to 0

        # Iterate until the specified number of iterations is reached or until convergence
        while iterations is None or iteration < iterations:

            # Increment the iteration counter
            iteration += 1  

            # Apply a single utility update using the update method
            if self.update(tolerance):
                # If convergence is reached, exit the loop
                break  

        # Return the total number of iterations performed
        return iteration  
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        # if current state is terminal then return None
        if self.mdp.is_terminal(state):
            return None
        
        # Define a function to calculate the Bellman equation for a specific action
        def calculate_bellman_equation(action):
            # Find next states (successors) based on the action
            successors = self.mdp.get_successor(state, action)

            # Initialize the sum to zero
            utility_sum = 0

            # Perform the Bellman equation on the successors
            for successor in successors:
                # Get the reward for the current state, action, and successor
                reward = self.mdp.get_reward(state, action, successor)
                
                # Calculate the discounted utility for the successor
                discounted_utility = self.discount_factor * self.utilities[successor]

                # Update the utility sum using the Bellman equation
                utility_sum += successors[successor] * (reward + discounted_utility)

            return utility_sum

        # get all actions for the current state
        actions = self.mdp.get_actions(state)
        
        # create temp array to store utilities to choose the action that leads to the max utility
        utilities = []
        
        # Iterate over all actions to calculate utilities
        for action in actions:

            # Calculate utility using the defined function
            utility_sum = calculate_bellman_equation(action)
           
            # store it in the temp array
            utilities.append(utility_sum)
        
        # Find the arg max action
        max_item = 0
        for i in range(len(utilities)):
            if utilities[i] > utilities[max_item]:
                max_item = i
        
        # Return the action that leads to the max utility
        return actions[max_item]

    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
