def char_frequency(s: str) -> dict:
    """
    Calculate the frequency of each character in a string (case-insensitive).

    Args:
        s (str): The input string.

    Returns:
        dict: A dictionary with characters as keys and their frequencies as values.
    """
    input_string = s.lower()
    freq = {}
    for char in input_string:
        freq[char] = freq.get(char, 0) + 1
    return freq

S = str(input("Enter a string: "))
result = char_frequency(S)
print("Character frequencies:", result)