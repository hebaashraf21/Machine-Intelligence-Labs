import math
from sokoban import AllSokobanActions, SokobanLayout, SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented
from typing import Tuple
import heapq
from collections import defaultdict
# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#TODO: Import any modules and write any functions you want to use

# def is_deadlock(state, layout):
#     # Extract the dimensions of the grid
#     height, width = layout.height, layout.width

#     # Check if the state is empty or the walkable positions don't cover the entire grid
#     if not state or len(state.layout.walkable) != height * width:
#         # If the state is empty or walkable positions are incomplete, there's no deadlock
#         return False

#     def find_boxes_and_goals(state, layout):
#         # Helper function to find positions of boxes, goals, and player
#         boxes, goals, player = [], [], None

#         # Iterate through the grid to find boxes, goals, and player
#         for row in range(layout.height):
#             for col in range(layout.width):
#                 char = state.layout.get_char_at(Point(row, col))
#                 if char == '$':
#                     boxes.append((row, col))
#                 elif char == '.':
#                     goals.append((row, col))
#                 elif char == '@':
#                     player = (row, col)

#         return boxes, goals, player

#     def is_corner_deadlock(box):
#         # Check if the box is in a corner and surrounded by walls
#         bx, by = box
#         box_position = bx * width + by
#         for pos in [(bx - 1, by), (bx + 1, by), (bx, by - 1), (bx, by + 1)]:
#             if state.layout.walkable(Point(*pos)) == '#':
#                 # If the box is in a corner surrounded by walls, it's a deadlock
#                 return True
#         return False

#     def is_double_box_deadlock(box):
#         # Check for a deadlock when two boxes are close to each other
#         bx, by = box
#         double_box_positions = [
#             (0, -1),
#             (0, 1),
#             (-1, 0),
#             (1, 0),
#         ]

#         # Iterate over possible positions for a second box relative to the first
#         for pos in double_box_positions:
#             # Create a set of walkable characters at the specified positions
#             pos_set = set(state.layout.walkable(Point(bx + dir % width, by + dir // width)) for dir in pos)

#             # Check if the set matches any of the deadlock conditions
#             if pos_set in ({'@', '+'}, {'@'}, {'@', '$'}, {'@', '$', '+'}):
#                 # If a deadlock condition is met, return True
#                 return True
#         return False

#     def is_too_many_boxes_deadlock(position_range):
#         # Count the number of boxes and goals in the specified range
#         box_count = goal_count = 0

#         # Iterate over the positions in the specified range
#         for i in position_range:
#             # Check the walkable character at each position
#             if state.layout.walkable(Point(i % width, i // width)) in {'@'}:
#                 # If a box is found, increment the box count
#                 box_count += 1
#             elif state.layout.walkable(Point(i % width, i // width)) in {'.'}:
#                 # If a goal is found, increment the goal count
#                 goal_count += 1

#         # Check if there are too many boxes compared to goals in the range
#         return box_count > goal_count

#     # Obtain the positions of boxes, goals, and player
#     boxes, goals, player = find_boxes_and_goals(state, layout)

#     # Check for deadlock conditions for each box
#     for box in boxes:
#         if is_corner_deadlock(box) or is_double_box_deadlock(box):
#             # If a deadlock condition is met for any box, return True
#             return True

#     # Check for deadlock conditions based on the specified range
#     for r in [range(width + 1, 2 * width - 1),
#               range(width * (height - 2) + 1, width * (height - 2) + width - 1),
#               range(width + 1, width * (height - 1) + 1, width),
#               range(2 * width - 2, width * height - 2, width)]:
#         if is_too_many_boxes_deadlock(r):
#             # If a deadlock condition is met in the specified range, return True
#             return True

#     # If no deadlock conditions are met, return False
#     return False



def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:

    # Check if the root is already the goal state
    if problem.is_goal(state):
        return 0

    # Use a priority queue to efficiently find the nearest goal for each crate
    crate_distances = []
    for crate in state.crates:

        # Find the minimum distance among all the calculated distances
        goal_distance = min([manhattan_distance(crate, goal) for goal in state.layout.goals])

        # Push the minimum distance onto the crate_distances heap using heapq
        # This heap will help efficiently find the nearest goal for each crate
        heapq.heappush(crate_distances, goal_distance)

    # Integrate deadlock penalty into the heuristic
    deadlock_penalty = 0
    # if is_deadlock(state, state.layout):
    #     deadlock_penalty = 1000  

    # Ensure the heuristic is consistent by taking the sum
    return sum(crate_distances) + deadlock_penalty
 