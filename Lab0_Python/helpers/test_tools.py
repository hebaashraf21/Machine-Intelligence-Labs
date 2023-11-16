from .utils import Result
from typing import Tuple, List

def read_text_file(file_path: str) -> str:
    with open(file_path, 'r') as f:
        return f.read()

def read_word_list(file_path: str) -> List[str]:
    with open(file_path, 'r') as f:
        return [line.lower().strip() for line in f.readlines()]

def compare_decipher(output: Tuple[str, int, int], expected_file_path: str, expected_shift: int, expected_wrong: int, log_path: str) -> Result:
    if not isinstance(output, tuple):
        return Result(False, 0, f"Wrong result type. Expected a tuple, Got a {type(output)}")
    if len(output) != 3:
        return Result(False, 0, f"Wrong result tuple size. Expected a tuple of 3 elements, Got a tuple of {len(output)} elements")
    deciphered, shift, wrong = output
    if expected_shift != shift:
        return Result(False, 0, f"Wrong result for the Caesar-Cipher Shift. Expected: {expected_shift}, Got: {shift}")
    if expected_wrong != wrong:
        return Result(False, 0, f"Wrong result for number of words not found in dictionary. Expected: {expected_wrong}, Got: {wrong}")
    
    if not isinstance(deciphered, str):
        return Result(False, 0, f"Wrong type of deciphered text. Expected a str, Got a {type(deciphered)}")

    expected_text = read_text_file(expected_file_path)
    if expected_text != deciphered:
        with open(log_path, 'w') as f:
            f.write(deciphered)
        message = "Wrong deciphered text.\n"
        message += f"You output was saved to '{log_path}'. You should compared it with expected result in '{expected_file_path}'."
        return Result(False, 0, message)
    
    return Result(True, 1, "")
    

    