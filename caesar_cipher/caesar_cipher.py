"""
Program Execution:
  python caesar.py encrypt <text_file> <letter>
  python caesar.py decrypt <text_file> <letter>
  python caesar.py crack <text_file> <English_frequencies_file>

Description: Caesar cipher program that can encrypt (shift text by offset key),
decrypt (shift back the text by a key), and crack text files (try all shifts
and select the best English text).
"""

import sys


def string_to_symbol_list(message: str) -> list[int]:
    """
    Description: Converts a string to a symbol list, where each element of the
    list is an integer encoding of the corresponding element of the string.
    Input: the message text to be converted
    Output: the encoding of the message into a list of integers
    """

    res = list()
    for i in message.upper():
        if "A" <= i <= "Z":
            res.append(ord(i) - 65)
        else:
            res.append(ord(i) - 65)
    return res


def symbol_list_to_string(symbol_list: list[int]) -> str:
    """
    Description: Converts a list of symbols to a string, where each element
    of the list is an integer encoding of the corresponding element of the string.
    Input: integer encoding of the message, stored in a list of integers
    Output: the message text as a string
    """

    res = ""
    for i in symbol_list:
        if 0 <= i <= 25:
            res += (chr(i + 65))
        else:
            res += chr(i + 65)
    return res


def shift(symbol: int, offset: int) -> int:
    """
    Description: Shifts the letter symbol to the right by an offset,
    where non-letters are not changed.
    Input: coded letter or non-letter code and an offset
    Output: shifted letter symbol or the same non-letter symbol
    """

    if 0 <= symbol <= 25:
        return (symbol + offset) % 26
    return symbol


def unshift(symbol: int, offset: int) -> int:
    """
    Description: Shifts the letter symbol to the left by an offset,
    where non-letters are not changed.
    Input: letter symbol or non-letter symbol and an offset to unshift
    Output: unshifted letter symbol or the same non-letter symbol
    """

    if 0 <= symbol <= 25:
        return (symbol - offset) % 26
    return symbol


def encrypt(message: str, key: int) -> str:
    """
    Description: Encrypts message using Caesar shift. First converts message
    to symbols, then shifts letter by key, and then converts it back.
    Input: Message/text and the key/shift
    Output: encrypted message
    """

    symbols = string_to_symbol_list(message)
    shifted_list = []
    for i in symbols:
        shifted_list.append(shift(i, key))
    return symbol_list_to_string(shifted_list)


def decrypt(cipher: str, key: int) -> str:
    """
    Description: Decrypts message using Caesar shift. First converts message
    to symbols, then unshifts letter by key, and then converts it back.
    Input: cipher text and key/numeric shift
    Output: decrypted message string
    """

    symbols = string_to_symbol_list(cipher)
    unshifted_list = []
    for i in symbols:
        unshifted_list.append(unshift(i, key))
    return symbol_list_to_string(unshifted_list)


def get_letter_frequencies(frequencies_filename: str) -> list[float]:
    """
    Description: Opens the frequencies file for the 26 letters in the alphabet,
    and reads floats, creating a list of frequencies, in order.
    Input: filename frequencies string
    Output: list of floats for the frequencies of A - Z
    """

    frequencies = []
    file = open(frequencies_filename, "r")
    for i in range(26):
        line = file.readline().strip()
        frequencies.append(float(line))
    file.close()
    return frequencies


def find_frequencies(symbols: list[int]) -> list[float]:
    """
    Description: Finds the frequencies of the letters in the symbol list.
    Does this by dividing the letter count by the total amount of letters.
    Input: list of symbol integers
    Output: List of frequencies for the letters A-Z
    """

    letter_count = [0] * 26
    total_letters = 0

    for i in symbols:
        if 0 <= i <= 25:
            letter_count[i] += 1
            total_letters += 1

    frequencies = []
    for j in letter_count:
        if total_letters > 0:
            frequency = j / total_letters
        else:
            frequency = 0
        frequencies.append(frequency)
    return frequencies


def score_frequencies(
    expected_frequencies: list[float], actual_frequencies: list[float]
) -> float:
    """
    Description: Scores the frequencies by comparing letter frequencies to the
    frequency they show up in the English language. This is done by finding
    the absolute value difference between these two values.
    Input: expected and actual frequencies lists
    Output: float of total score
    """

    total_score = 0
    for i in range(26):
        total_score += abs(expected_frequencies[i] - actual_frequencies[i])
    return total_score


def crack(text: str, frequencies_filename_English: str) -> str:
    """
    Description: Cracks the Caesar cipher message without a key. This is done
    by testing all the possible shifts. For every shift, the text is decrypted,
    the letter frequency is computed, compared to the reference frequencies,
    and the text with the lowest score is chosen.
    Input: text to crack and the frequencies filename to read
    Output: the decrypted message with the best score
    """

    expected_frequencies = get_letter_frequencies(frequencies_filename_English)
    ideal_score = float("inf")
    ideal_text = ""

    for i in range(26):
        decrypted_text = decrypt(text, i)
        symbols = string_to_symbol_list(decrypted_text)
        actual_frequencies = find_frequencies(symbols)
        score = score_frequencies(expected_frequencies, actual_frequencies)

        if score < ideal_score:
            ideal_score = score
            ideal_text = decrypted_text
    return ideal_text


def main():
    """
    Description: Reads the files inputted by the user, and encrypts, decrypts,
    or cracks the message based on the user input.
    Input: User input in terminal
    Output: encrypted, decrypted, or cracked message
    """

    filename = sys.argv[2]
    file = open(filename, "r")
    text = file.read()
    file.close()

    function = sys.argv[1]
    if function == "encrypt":
        key = ord(sys.argv[3].upper()) - 65
        print(encrypt(text, key))
    elif function == "decrypt":
        key = ord(sys.argv[3].upper()) - 65
        print(decrypt(text, key))
    elif function == "crack":
        frequencies_filename_English = sys.argv[3]
        result = crack(text, frequencies_filename_English)
        print(result)


if __name__ == "__main__":
    main()