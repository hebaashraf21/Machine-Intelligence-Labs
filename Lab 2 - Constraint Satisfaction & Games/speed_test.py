import time

def math_test(steps: int = int(1e7), verbose: bool = False) -> float:
    # This speed test approximates PI
    # by integrating the arc length of the function sqrt(1 - x^2) over x in [0, 1] to get PI/2
    start = time.time()

    arc_length = 0
    x, y = 0, 1
    for index in range(1, steps+1):
        new_x = index / steps
        new_y = (1 - new_x * new_x) ** 0.5
        dx = new_x - x
        dy = new_y - y
        arc_length += (dx * dx + dy * dy) ** 0.5
        x, y = new_x, new_y
    pi = 2 * arc_length

    elapsed = time.time() - start

    if verbose: print(f"Math Test: Done in {elapsed} seconds")
    
    return elapsed

def sort_test(size: int = int(1e7), verbose: bool = False) -> float:
    import random

    start = time.time()

    random.seed(123)
    data = [random.randint(0, 1000) for _ in range(size)]
    data.sort()

    elapsed = time.time() - start

    if verbose: print(f"Sort Test: Done in {elapsed} seconds")
    
    return elapsed

def warm_up():
    math_test(int(1e5))
    sort_test(int(1e5))

math_reference_time = 12
sort_reference_time = 24

def speed_test() -> float:
    math_time = math_test(verbose=True)
    sort_time = sort_test(verbose=True)
    multiplier = min([math_time / math_reference_time, sort_time / sort_reference_time])
    return multiplier

def get_time_limit_multiplier(overwrite: bool = False):
    import os, json
    file_name = "time_config.json"
    if not overwrite and os.path.exists(file_name):
        return json.load(open(file_name, 'r'))["multiplier"]
    else:
        print("Measuring the speed of your machine...")
        warm_up()
        multiplier = speed_test()
        if multiplier < 1:
            print(f"Your machine is {1.0/multiplier} times faster than the grading machine. Time limits will be decreased accordingly.")
        elif multiplier > 1:
            print(f"Your machine is {multiplier} time slower than the grading machine. Time limits will be increased accordingly.")
        json.dump({'multiplier':multiplier}, open(file_name, 'w'), indent=2)
        return multiplier

if __name__ == "__main__":
    get_time_limit_multiplier(overwrite=True)