from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass

"""
Environment Description:
    The snake is a 2D grid world where the snake can move in 4 directions.
    The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
    The snake can wrap around the grid.
    The snake can eat apples which will grow the snake by 1.
    The snake can not eat itself.
    You win if the snake body covers all of the level (there is no cell that is not occupied by the snake).
    You lose if the snake bites itself (the snake head enters a cell occupied by its body).
    The action can not move the snake in the opposite direction of its current direction.
    The action can not move the snake in the same direction 
        i.e. (if moving right don't give an action saying move right).
    Eating an apple increases the reward by 1.
    Winning the game increases the reward by 100.
    Losing the game decreases the reward by 100.
"""

# IMPORTANT: This class will be used to store an observation of the snake environment
@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]     # The points occupied by the snake body 
                            # where the head is the first point and the tail is the last  
    direction: Direction    # The direction that the snake is moving towards
    apple: Optional[Point]  # The location of the apple. If the game was already won, apple will be None


class SnakeEnv(Environment[SnakeObservation, Direction]):

    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:
        """
        Generates and returns a random apple position which is not on a cell occupied 
        by the snake's body.
        """
        snake_positions = set(self.snake)
        possible_points = [Point(x, y) 
            for x in range(self.width) 
            for y in range(self.height) 
            if Point(x, y) not in snake_positions
        ]
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> SnakeObservation:
        if seed is not None:
            self.rng.seed(seed)

        # Initialize the snake at the center and set the direction to LEFT
        center_x = self.width // 2
        center_y = self.height // 2
        self.snake = [Point(center_x, center_y)]
        self.direction = Direction.LEFT

        # Generate the initial apple position
        self.apple = self.generate_random_apple()

        return SnakeObservation(tuple(self.snake), self.direction, self.apple)

    def actions(self) -> List[Direction]:
        # a snake can wrap around the grid
        # NOTE: The action order does not matter

        # If the snake is currently moving vertically (UP or DOWN),
        if self.direction in [Direction.UP, Direction.DOWN]:
            # It can change its direction to LEFT, RIGHT, or keep moving in the current direction (NONE).
            return [Direction.LEFT, Direction.RIGHT, Direction.NONE]
        # If the snake is currently moving horizontally (LEFT or RIGHT),
        elif self.direction in [Direction.LEFT, Direction.RIGHT]:
            # It can change its direction to UP, DOWN, or keep moving in the current direction (NONE).
            return [Direction.UP, Direction.DOWN, Direction.NONE]
        # If the snake's current direction is not recognized (this should not happen in a valid game),
        else:
            # It can choose any direction, including UP, DOWN, LEFT, RIGHT, or keep moving in the current direction (NONE).
            return [Direction.UP, Direction.DOWN, Direction.LEFT, Direction.RIGHT]

    def step(self, action: Direction) -> Tuple[SnakeObservation, float, bool, Dict]:

        # Helper function to wrap around the snake's head position
        def wrap_around(position: Point) -> Point:
            x = (position.x + self.width) % self.width
            y = (position.y + self.height) % self.height

            # Check if the wrapped position is within the snake
            if Point(x, y) in self.snake:
                x = position.x
                y = position.y

            return Point(x, y)

        # Update the direction of the snake based on the chosen action
        if action != Direction.NONE:
            # Avoid moving in the opposite direction or the same direction
            if action != -self.direction and action != self.direction:
                self.direction = action
        else:
            action=self.direction

        # Move the snake in the current direction
        head = self.snake[0]
        new_head = head + self.direction.to_vector()

        # Wrap around if the new_head is outside the grid
        new_head = wrap_around(new_head)

        # Initialize 'done' variable
        done = False
        # Initialize 'reward' variable  
        reward = 0  

        # Check for winning condition (snake occupies the entire grid)
        if len(self.snake) == self.width * self.height:
            # Increase the reward for winning
            reward += 100
            done = True

        # Check for collisions with the apple
        if new_head == self.apple:
            # Move the snake
            self.snake.insert(0, new_head)
            # Generate a new apple
            self.apple = self.generate_random_apple()

            if self.apple is None:
                # No available empty cells for the apple, end the episode
                done = True
            else:
                # Increase the reward for eating the apple
                reward += 1
        else:
            # Move the snake
            self.snake.insert(0, new_head)
            #Remove the tail
            self.snake.pop()

            # Check for collisions with itself
            if new_head in self.snake[1:]:
                # Decrease the reward for collision
                reward -= 100
                done = True

        observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)
        return observation, reward, done, {}

    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end='')
                elif p in self.snake:
                    print('*', end='')
                elif p == self.apple:
                    print('$', end='')
                else:
                    print('.', end='')
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake), 
            self.parse_action(direction), 
            Point(*apple)
        )
    
    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))
    
    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            'R': Direction.RIGHT,
            'U': Direction.UP,
            'L': Direction.LEFT,
            'D': Direction.DOWN,
            '.': Direction.NONE,
        }[string.upper()]
    
    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: 'R',
            Direction.UP:    'U',
            Direction.LEFT:  'L',
            Direction.DOWN:  'D',
            Direction.NONE:  '.',
        }[action]