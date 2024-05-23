from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented
import copy

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #TODO: Write this function

    # Loop over all problem constraints
    for constraint in problem.constraints:
        # Check only binary constraints involving the assigned variable
        if isinstance(constraint, BinaryConstraint) and assigned_variable in constraint.variables:

            # Get the other variable in the constraint with the assigned_variable
            other_variable = constraint.get_other(assigned_variable)

            # Skip constraints involving an assigned variable
            if other_variable not in domains:
                continue

            # Copy the other variable's domain
            other_domain = domains[other_variable].copy()

            # Update the other variable's domain based on the binary constraint
            new_domain = {value for value in other_domain if constraint.condition(assigned_value, value)}
            domains[other_variable] = new_domain

            # If the other variable's domain becomes empty, return False
            if not new_domain:
                return False

    # If all updates were successful, return True
    return True


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #TODO: Write this function

    # create a list to store tuple of (values that removes values from other variables , the number of removed values)
    restraining_values = []  

    # get the domain of the variable to assign
    values = domains[variable_to_assign]  

    # Loop over the domain of the variable to assign to check each value 
    for value in values:  

        # create a variable to store the number of removed values, initially 0
        removed_values = 0  
        
        # check each constraint in the problem
        for constraint in problem.constraints:  

            # Check only binary constraints involving the assigned variable
            if isinstance(constraint, BinaryConstraint) and (variable_to_assign in constraint.variables):

                # get the other variable in the constraint besides the variable to assign
                other_variable = constraint.get_other(variable_to_assign) 

                # check if the other variable has a domain
                if domains.get(other_variable) is not None:  

                    # check each value in the domain of the other variable
                    for other_value in domains[other_variable]:  

                        # create a dictionary with the variable to assign and its value and the other variable and its value
                        dicty = {variable_to_assign: value, other_variable: other_value}
                        
                        # check if the dictionary is not consistent with the constraints
                        if not constraint.is_satisfied(dicty): 

                            # if not, increment the number of removed values, don't remove them from the domain of the other variable 
                            removed_values += 1 

        # add the value and the number of removed values to the list of restraining values
        restraining_values.append((value, removed_values))  

    # sort the list of restraining values based on the number of removed values for each value and then the value itself
    # sort according to the number of removed values first and then the value itself to make sure that the values with the same number of removed values are sorted in ascending order
    restraining_values.sort(key=lambda x: (x[1], x[0]))

    # return the list of sorted values in the list of restraining values
    return [x[0] for x in restraining_values]  

# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    def recursive_solve(domains: Dict, assignment: Assignment = {}) -> Optional[Assignment]:
        # Return None if the problem is not 1-consistent
        if not one_consistency(problem):
            return None

        # Return the assignment if it is complete
        if problem.is_complete(assignment):
            return assignment

        # Choose the variable with the minimum remaining values to be assigned
        current_variable = minimum_remaining_values(problem, domains)
        
        # Choose the domain of the variable based on the "least restraining value" heuristic
        values = least_restraining_values(problem, current_variable, domains)

        for value in values:
            # Copy the assignment and the domains
            assignment_copy = assignment.copy()
            assignment_copy[current_variable] = value

            domains_copy = domains.copy()
            del domains_copy[current_variable]

            # Check if the assignment is consistent with the constraints    
            if forward_checking(problem, current_variable, value, domains_copy):
                # Call the recursive function
                result = recursive_solve(domains_copy, assignment_copy)
                
                # Return the result assignment if it is not None
                if result is not None:
                    return result
        return None

    # Call the recursive function
    return recursive_solve(problem.domains)
    