# This is a Pseudo Random Number Generator using the Mersene Twister Algorithm
from typing import List, Optional, Any


class RandomGenerator:
    __N = 624

    def __init__(self, seed: Optional[int] = None) -> None:
        self.table = [0] * RandomGenerator.__N
        self.seed(seed)

    def seed(self, seed: Optional[int] = None):
        """Initializes the generators using the given seed.
        
        Args:
            seed (Optional[int]): The seed used for initialization. If None, the current time is used. (default: None)
        """
        if seed is None:
            import time
            seed = time.time_ns()
        self.table[0] = seed
        for i in range(1, RandomGenerator.__N):
            temp = 1812433253 * (self.table[i-1] ^ (self.table[i-1] >> 30)) + i
            self.table[i] = temp & 0xffffffff
        self.index = RandomGenerator.__N+1

    def __twist(self):
        for i in range(0, RandomGenerator.__N):
            x = (self.table[i] & 0x80000000) + (self.table[(i+1) % RandomGenerator.__N] & 0x7FFFFFFF)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ 0x9908B0DF
            self.table[i] = self.table[(i + 397) % RandomGenerator.__N] ^ xA

    def generate(self) -> int:
        """Generates a pseudorandom 32-bit integer.
        
        Returns:
            generate (int): A pseudorandom 32-bit integer.
        """
        if self.index >= RandomGenerator.__N:
            self.__twist()
            self.index = 0

        y = self.table[self.index]
        y = y ^ ((y >> 11) & 0xFFFFFFFF)
        y = y ^ ((y << 7) & 0x9D2C5680)
        y = y ^ ((y << 15) & 0xEFC60000)
        y = y ^ (y >> 18)

        self.index += 1
        return y & 0xffffffff
    
    def int(self, l: int, u: int) -> int:
        """Generates a uniform pseudorandom integer in the range [l, u] (inclusive).
        
        Args:
            l (int): The lower bound of the range.
            u (int): The upper bound of the range.
        
        Returns:
            int (int): A uniform pseudorandom integer in the range [l, u] (inclusive).
        """
        assert l <= u, f"the lower bound must be less then or equal the upper bound, got {l=} nd {u=}"
        if l == u: return l
        return l + self.generate() % (u - l + 1)

    def float(self, l: float = 0, u: float = 1) -> float:
        """Generates a uniform pseudorandom floating-point number in the range [l, u] (inclusive).
        
        Args:
            l (float): The lower bound of the range.
            u (float): The upper bound of the range.
        
        Returns:
            float (float): A uniform pseudorandom floating-point number in the range [l, u] (inclusive).
        """
        return (self.generate() / 0xffffffff) * (u - l) + l
    
    def sample(self, weights: List[float]) -> int:
        """Samples an integer `i` in the range [0, len(weights)-1] with a probability proportional to `weights[i]`.
        
        Args:
            weights (List[float]): The unnormalized probabilities where `weights[i]` is proportional to the likelihood of sampling `i`.
        
        Returns:
            sample (int): The randomly sampled integer.
        """
        random = self.float(0, sum(weights))
        cumulative = 0
        for index, weight in enumerate(weights):
            cumulative += weight
            if random <= cumulative:
                return index
        return len(weights)-1
    
    def choice(self, items: List[Any]) -> Any:
        """Randomly chooses an item from `items` with equal probability.
        
        Args:
            items (List[Any]): The list of items to choose from.
        
        Returns:
            choice (Any): the selected item.
        """
        return items[self.int(0, len(items)-1)]

if __name__ == "__main__":
    rng = RandomGenerator(0)
    prob = [0.8, 0.1, 0.1]
    freq = [0]*len(prob)
    iterations = 10000
    for _ in range(iterations):
        freq[rng.sample(prob)] += 1
    print([f/iterations for f in freq])
