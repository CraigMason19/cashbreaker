#-------------------------------------------------------------------------------
# Name:        en_words.py
#
# Notes:       A collection of methods for reading and interacting with a text 
#              file containing words in a dictionary. Also contains methods for
#              working with words. 
#
#              Makes use of a sorted dictionary (sorted by length as well as 
#              alphabetically) for faster lookups, a helper function
#              called create_sorted_dict will create one from a normal 
#              alphabetised dictionary.
#
# Links:        
#
# TODO:        
#
#-------------------------------------------------------------------------------

import os

# region Globals
_PATH = os.path.dirname(__file__)
_NAME = 'en_words'

_FILENAME = _PATH + "\\" + _NAME + ".txt"
_FILENAME_SORTED = _PATH + "\\" + _NAME + "_sorted.txt"

# Guess characters e.g. s?a_d -> salad
MISSING_CHARACTERS = '?-_.' 

#endregion

def create_sorted_dict(filename=_FILENAME, filename_sorted=_FILENAME_SORTED):
    """ Reads a dictionary in alphabetical order and then creates a file that is 
        sorted by length and then alphabetically.

    Args:
        filename:
            The name of the file containing the dictionary.
        filename_sorted:
            The name of the file to create containing the sorted dictionary.

    Returns:
        None.
    """
    lines = None

    with open(filename) as f:
        lines = f.readlines()
        lines.sort(key=lambda item: (len(item), item)) # length then alphabetical
    
    with open(filename_sorted, 'w+') as f:
        for line in lines:
            f.write(line.lower())

# region Basic Reader functions

def unsorted_words(filename=_FILENAME):
    """ Returns a list of words from a dictionary not sorted by length.

    Args:
        filename:
            The name of the file containing the dictionary.

    Returns:
        A list of words.
    """
    with open(filename) as f:
        return f.read().lower().splitlines()

def unsorted_words_gen(filename=_FILENAME):
    """ A generator that returns a word from a dictionary not sorted by 
        length.

    Args:
        filename:
            The name of the file containing the dictionary.

    Returns:
        A generator.
    """
    with open(filename) as f:
        for line in f:
            yield line.lower().strip()

def sorted_words(filename_sorted=_FILENAME_SORTED):
    """ Returns a list of words from a dictionary sorted by length as well as
        alphabetically.

    Args:
        filename_sorted:
            The name of the file containing the sorted dictionary.

    Returns:
        A list.
    """
    with open(filename_sorted) as f:
        return f.read().lower().splitlines()

def sorted_words_gen(filename_sorted=_FILENAME_SORTED):
    """ A generator that returns a word from a dictionary sorted by 
        length and alphabetically.

    Args:
        filename_sorted:
            The name of the file containing the sorted dictionary.

    Returns:
        A generator.
    """
    with open(filename_sorted) as f:
        for line in f:
            yield line.lower().strip()

def word_count(filename=_FILENAME):
    """ Returns the number of words in the dictionary.

    Args:
        filename:
            The name of the file containing the dictionary.

    Returns:
        A int.
    """
    counter = 0

    for word in sorted_words_gen(filename):
        counter += 1

    return counter

def find_largest_word(filename=_FILENAME):
    """ Returns the largest word in the dictionary. If there is no largest word, 
        the first word of largest length is returned.

    Args:
        filename:
            The name of the file containing the dictionary.

    Returns:
        A string.
    """
    max_word = ""

    for word in unsorted_words_gen(filename):
        if len(word) > len(max_word):
            max_word = word

    return max_word.lower()

# endregion

#region Word Finder functions 

def words_of_length(length=3, filename_sorted=_FILENAME_SORTED):
    """ Returns a list of all words of a certain length.

    Args:
        length:
            The minimum number of letters to find.
        filename_sorted:
            The name of the file containing the sorted dictionary.

    Returns:
        A list.
    """
    if length < 0:
        return []
 
    words = []

    for word in sorted_words_gen(filename_sorted):
        letter_count = len(word)

        if letter_count > length:
                break

        elif letter_count == length:
            words.append(word.lower())

    return words

def words_of_length_gen(length=3, filename_sorted=_FILENAME_SORTED):
    """ Returns a generator for finding all words of a certain length.

    Args:
        length:
            The minimum number of letters to find.
        filename_sorted:
            The name of the file containing the sorted dictionary.

    Returns:
        A generator.
    """    
    if length < 0:
        return []

    for word in sorted_words_gen(filename_sorted):
        letter_count = len(word)

        if letter_count > length:
            break

        elif letter_count == length:
            yield word.lower()
 
def is_potential_match(partial_word, potential_word, ignore_letters='', required_letters=''):
    """ Compares two words to check if the words are a potential match. Returns 
        True if they are and False otherwise.

        E.g. is_potential_match("??ttl-", "battle", 'x', 'b') == True
             is_potential_match("??ttl-", "battle", 'xe', 'b') == False

    Args:
        partial_word:
            A word with letters missing (represented by MISSING_CHARACTERS global variable).
        potential_word:
            A word to compare.
        ignore_letters:
            A string of letters not needed.
        required_letters:
            A string of letters that are required.

    Returns:
        A bool.
    """ 
    partial_word, potential_word = partial_word.lower(), potential_word.lower()
    ignore_letters, required_letters = ignore_letters.lower(), required_letters.lower()

    # Check that the potential word has the required letters 
    for rl in required_letters:
        if rl not in potential_word:
            return False

    # If it does, compare each letter one at a time
    for letter_a, letter_b in zip(partial_word, potential_word):
        # Letter in second word is not allowed
        if letter_b in ignore_letters:
            return False

        # Unknown letter, go to the next
        elif letter_a in MISSING_CHARACTERS:
            continue

        # Not a match
        elif letter_a != letter_b:
            return False

    return True

def potential_words(partial_word, ignore_letters='', required_letters='', filename_sorted=_FILENAME_SORTED):
    """ Compares a partial word against the words inside the sorted dictionary. Returns a list
        of all potential matches. 

    Args:
        partial_word:
            A word with letters missing (represented by MISSING_CHARACTERS global variable).
        ignore_letters:
            A string of letters not needed.
        required_letters:
            A string of letters that are required.
        filename_sorted:
            The name of the file containing the sorted dictionary.

    Returns:
        A list of words.
    """ 
    partial_word = partial_word.lower()
    ignore_letters, required_letters = ignore_letters.lower(), required_letters.lower()
    
    words = []

    for potential_word in words_of_length_gen(len(partial_word), filename_sorted):
        if is_potential_match(partial_word, potential_word, ignore_letters, required_letters):
            words.append(potential_word.lower())

    return words

def letters_in_word(letters, word, remove_doubles=False):
    """ Checks that letters are in a word.

    Args:
        letters:
            A string of letters that are in a word.
        word:
            The word to check.
        remove_doubles:
            A bool to allow for / against double letters.

    Returns:
        A bool.
    """ 

    # Words with unique characters
    if remove_doubles:
        if len(set(word)) != len(word):
            return False

    for letter in word:
        if letter not in letters:
            return False
        
    return True

def words_from_letters(letters, min_len=3, max_len=6, remove_doubles=False, filename_sorted=_FILENAME_SORTED):
    """ Finds a list of words that contains certain letters.

    Args:
        letters:
            A string of letters that are in a word.
        min_len:
            The minimum word length.
        max_len:
            The maximum word length.
        remove_doubles:
            A bool to allow for / against double letters.

    Returns:
        A list.
    """ 
    letters = letters.lower()    
    words = []

    if min_len == None or min_len == 0:
        min_len = 1

    for word in sorted_words_gen(filename_sorted):
        if len(word) < min_len:
            continue

        # If there is no max_len just carry on, otherwise stop
        if max_len == None:
            pass
        else:
            if len(word) > max_len:
                break

        if letters_in_word(letters, word, remove_doubles):
            words.append(word.lower())

    return(words)

# endregion

def main():
    """
    Example usage
    """
    sd = create_sorted_dict()

    print("Default dictionary")
    print(f"Name:")
    print(f"\t{_FILENAME}")

    print(f"\nWord count:") # 194433
    print(f"\t{word_count()}")

    largest = find_largest_word()
    print(f"\nLargest word ({len(largest)}):")
    print(f"\t{largest}")

    wol = words_of_length(4)
    print(f"\nWords of len(4):") # 5368
    print(f"\t{len(wol)}")  

    word = '_?tt-e'
    pw = potential_words(word)
    print(f"\nPotential words of {word}: {len(pw)}") 
    print(f"\t{pw}")  

    letters = "beetles"
    words = words_from_letters(letters, min_len=3, max_len=5)
    print(f"\nWords from letters '{letters}' between 3 & 5 letters: {len(words)}") 
    print(f"\t{words[:20]}...")
    # print(f"\t{words}")  

    letters = "beetles"
    words = words_from_letters(letters, min_len=5, max_len=None, remove_doubles=False) 
    print(f"\nWords from letters '{letters}' between 5 & NONE letters: {len(words)}") 
    print(f"\t{words[:20]}...")
    # print(f"\t{words}")  

if __name__ == '__main__':
    main()