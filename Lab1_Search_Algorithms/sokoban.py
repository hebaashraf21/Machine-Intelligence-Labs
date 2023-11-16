from dataclasses import dataclass
from typing import FrozenSet, Iterable
from enum import Enum

from mathutils import Direction, Point
from problem import Problem
from helpers.utils import track_call_count

# This file contains the definition for the Sokoban problem
# In this problem, the agent can move Up, Down, Left or Right
# and it has to push all the crates till every crate is on a goal.

# This enum represents all the possible tiles in a Sokoban map
class SokobanTile(str, Enum):
    EMPTY  = " "
    WALL   = "#"
    CRATE  = "$"
    GOAL   = "."
    PLAYER = "@"
    CRATE_ON_GOAL  = "*"
    PLAYER_ON_GOAL = "+"

# For the sokoban state, we use dataclass to automatically implement:
#   the constructor and to make the class immutable
# We disable the automatic equality implementation since we don't need it;
# we only need the default equality which compares objects by pointers.
# The layout contains the problem details that are unchangeable across states such as:
#   The walkable area (locations without walls) and the locations of the goals
@dataclass(eq=False, frozen=True)
class SokobanLayout:
    __slots__ = ("width", "height", "walkable", "goals")
    width: int
    height: int
    walkable: FrozenSet[Point]
    goals: FrozenSet[Point]

# For the sokoban state, we use dataclass with frozen=True to automatically implement:
#   the constructor, the == operator, the hash function and to make the class immutable
# Now it can be added to sets and used as keys in dictionaries
# This will contain a reference to the sokoban layout and it will contain environment details that change across states such as:
#   The player location and the locations of the crates 
@dataclass(frozen=True)
class SokobanState:
    __slots__ = ("layout", "player", "crates")
    layout: SokobanLayout
    player: Point
    crates: FrozenSet[Point]

    # This operator will convert the state to a string containing the grid representation of the level at the current state
    def __str__(self) -> str:
        def position_to_str(position):
            if position not in self.layout.walkable:
                return SokobanTile.WALL
            if position == self.player:
                return SokobanTile.PLAYER_ON_GOAL if position in self.layout.goals else SokobanTile.PLAYER
            if position in self.crates:
                return SokobanTile.CRATE_ON_GOAL if position in self.layout.goals else SokobanTile.CRATE
            if position in self.layout.goals:
                return SokobanTile.GOAL
            return SokobanTile.EMPTY
        return '\n'.join(''.join(position_to_str(Point(x, y)) for x in range(self.layout.width)) for y in range(self.layout.height))
    
    

# This is a list of all the possible actions for the sokoban agent
AllSokobanActions = [
    Direction.RIGHT,
    Direction.UP,
    Direction.DOWN,
    Direction.LEFT
]

# This is the implementation of the sokoban problem
class SokobanProblem(Problem[SokobanState, Direction]):
    # The problem will contain the sokoban layout and the inital state
    layout: SokobanLayout
    initial_state: SokobanState

    def get_initial_state(self) -> SokobanState:
        return self.initial_state

    def is_goal(self, state: SokobanState) -> bool:
        return self.layout.goals == state.crates

    # We use @track_call_count to track the number of times this function was called to count the number of explored nodes
    @track_call_count
    def get_actions(self, state: SokobanState) -> Iterable[Direction]:
        actions = []
        for direction in Direction:
            position = state.player + direction.to_vector()
            # Disallow walking into walls
            if position not in self.layout.walkable: continue
            # Check if walking into a crate
            if position in state.crates:
                # make sure that the crate is not pushed into a wall or another crate
                crate_position = position + direction.to_vector()
                if crate_position not in self.layout.walkable or crate_position in state.crates:
                    continue
            actions.append(direction)
        return actions

    def get_successor(self, state: SokobanState, action: Direction) -> SokobanState:
        player = state.player + action.to_vector()
        crates = state.crates
        if player not in self.layout.walkable:
            # If we try to walk into a wall, then this action is wrong
            raise Exception(f"Invalid action {action} in state:" + "\n" + str(state))
        if player in crates:
            crate_position = player + action.to_vector()
            if crate_position not in self.layout.walkable or crate_position in crates:
                # If we try to push a crate into a wall or another crate, then this action is wrong
                raise Exception(f"Invalid action {action} in state:" + "\n" + str(state))
            # If we walk to a crate, we push it
            crates = crates.symmetric_difference({player,crate_position})
        return SokobanState(state.layout, player, crates)

    def get_cost(self, state: SokobanState, action: Direction) -> float:
        # All actions have the same cost
        return 1

    # Read a sokoban problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'SokobanProblem':
        walkable, crates, goals =  set(), set(), set()
        player: Point = None
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != SokobanTile.WALL:
                    walkable.add(Point(x, y))
                    if char == SokobanTile.PLAYER:
                        player = Point(x, y)
                    elif char == SokobanTile.CRATE:
                        crates.add(Point(x, y))
                    elif char == SokobanTile.GOAL:
                        goals.add(Point(x, y))
                    if char == SokobanTile.PLAYER_ON_GOAL:
                        player = Point(x, y)
                        goals.add(Point(x, y))
                    elif char == SokobanTile.CRATE_ON_GOAL:
                        crates.add(Point(x, y))
                        goals.add(Point(x, y))
        problem = SokobanProblem()
        problem.layout = SokobanLayout(width, height, frozenset(walkable), frozenset(goals))
        problem.initial_state = SokobanState(problem.layout, player, frozenset(crates))
        return problem

    # Read a sokoban problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'SokobanProblem':
        with open(path, 'r') as f:
            return SokobanProblem.from_text(f.read())