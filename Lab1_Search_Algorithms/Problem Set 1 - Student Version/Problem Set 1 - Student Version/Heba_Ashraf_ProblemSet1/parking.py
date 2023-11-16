from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

ParkingState = Any
ParkingAction = Tuple[int, Direction]

class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]
    cars: Tuple[Point]
    slots: Dict[Point, int]
    width: int
    height: int

    def get_initial_state(self) -> ParkingState:
        # Return the initial state of the parking problem, which is the initial positions of the cars.
        return self.cars
    
    def is_goal(self, state: ParkingState) -> bool:

        # Iterate over each slot in the parking problem
        for point in self.slots:

            # Check if the position of the car in the given state is equal to the slot's position.
            if state[self.slots[point]] != point:
                return False
        return True
    
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
         # Initialize an empty list to store valid actions.
        actions = []

        # Iterate over each car in the given state.
        for car_index, car_position in enumerate(state):

            # Iterate over each possible direction (left, right, up, down).
            for direction in Direction:

                # Calculate the new position if the car moves in the current direction.
                new_position = car_position + direction.to_vector()

                # Check if the new position is within the passages and not occupied by another car.
                if new_position in self.passages and new_position not in state:

                    # If the conditions are met, add the action to the list of valid actions.
                    actions.append((car_index, direction))
        return actions


    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
         # Extract information from the given action.
        car_index, direction = action
        
        # Get the current position of the car in the given state.
        car_position = state[car_index]
        
        # Calculate the new position after performing the action.
        new_position = car_position + direction.to_vector()
        
        # Create a new list representing the updated state.
        new_state = list(state)
        
        # Update the position of the car in the new state.
        new_state[car_index] = new_position
        
        # Return the new state as a tuple.
        return tuple(new_state)

    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        # Extract information from the given action.
        car_index, direction = action
        
        # Calculate a base cost based on the car's index.
        cost = 26 - car_index
        
        # Get the current position of the car in the given state.
        current_car_position = state[car_index]
        
        # Calculate the new position after performing the action.
        new_car_position = current_car_position + direction.to_vector()
        
        # Check if the new position is a slot and if the car in that slot is not the current car.
        if new_car_position in self.slots and self.slots[new_car_position] != car_index:
            # If the conditions are met, add an additional cost of 100.
            cost += 100
        
        # Return the calculated cost.
        return cost
     
        
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())