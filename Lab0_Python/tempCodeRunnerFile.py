from typing import Tuple, List
import utils
from helpers.test_tools import read_text_file, read_word_list

'''
    The DecipherResult is the type defintion for a tuple containing:
    - The deciphered text (string).
    - The shift of the cipher (non-negative integer).
        Assume that the shift is always to the right (in the direction from 'a' to 'b' to 'c' and so on).
        So if you return 1, that means that the text was ciphered by shifting it 1 to the right, and that you deciphered the text by shifting it 1 to the left.
    - The number of words in the deciphered text that are not in the dictionary (non-negative integer).
'''
DechiperResult = Tuple[str, int, int]


def decipher_text(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('a') if char.islower() else ord('A')
            decoded_char = chr(
                (ord(char) - ascii_offset - shift) % 26 + ascii_offset)
            result += decoded_char
        else:
            result += char
    return result


def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    '''
        This function takes the ciphered text (string)  and the dictionary (a list of strings where each string is a word).
        It should return a DechiperResult (see above for more info) with the deciphered text, the cipher shift, and the number of deciphered words that are not in the dictionary. 

    '''

    best_shift = 0
    best_deciphered_text = ''
    best_invalid_words_count = float('inf')

    for shift in range(26):
        deciphered_text = decipher_text(ciphered, shift)
        words = deciphered_text.split()
        invalid_word_count = 0
        for word in words:
            if not word.lower() in dictionary:
                invalid_word_count += 1

        if invalid_word_count < best_invalid_words_count:
            best_invalid_words_count = invalid_word_count
            best_shift = shift
            best_deciphered_text = deciphered_text

    DechiperResult = (best_deciphered_text,
                      best_shift, best_invalid_words_count)
    return DechiperResult

    # utils.NotImplemented()
