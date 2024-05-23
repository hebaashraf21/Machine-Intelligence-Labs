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


# def decipher_text(text, shift):
#     result = ""
#     for char in text:
#         if char.isalpha():
#             ascii_offset = ord('a') if char.islower() else ord('A')
#             decoded_char = chr(
#                 (ord(char) - ascii_offset - shift) % 26 + ascii_offset)
#             result += decoded_char
#         else:
#             result += char
#     return result

def decipher_text(text, shift):
    ascii_offset = ord('a')
    result = [chr(ascii_offset + (ord(char) - ascii_offset - shift) %
                  26) if char.isalpha() else char for char in text]
    return ''.join(result)


def caesar_dechiper(ciphered: str, dictionary: List[str]) -> DechiperResult:
    best_shift = 0
    best_deciphered_text = ''
    best_invalid_words_count = float('inf')

    dictionary_set = set(word.lower() for word in dictionary)

    for shift in range(26):
        deciphered_text = decipher_text(ciphered, shift)
        deciphered_text = deciphered_text.lower()
        # for word in words:
        #     if not word.lower() in dictionary:
        #         invalid_words_count += 1
        invalid_words_count = sum(
            1 for word in deciphered_text.split() if word not in dictionary_set)

        if invalid_words_count == 0:
            return (deciphered_text, shift, invalid_words_count)

        if invalid_words_count < best_invalid_words_count:
            best_invalid_words_count = invalid_words_count
            best_shift = shift
            best_deciphered_text = deciphered_text

    return (best_deciphered_text, best_shift, best_invalid_words_count)

    # utils.NotImplemented()
