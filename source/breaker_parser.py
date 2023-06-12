#-------------------------------------------------------------------------------
# Name:        breaker_parser.py
#
# Notes:       Methods to load a cashbreaker from a file.
#
# Links:        
#
# TODO:        
#
#-------------------------------------------------------------------------------

"""
Custom cashbreak format

A simple .txt file format to represent the cashbreaker. There are 5 blocks split
up by an empty line. These blocks are comment, prize, given, guess & grid.

Examples are in the breakers folder.
"""

import numpy as np

class BreakerParseError(Exception):
    pass

def parse_prize_block(block):
    """ Parses a list of strings and returns a series of integers or None. 
        E.g. '23 22 16 14 26 17'

    Args:
        block:
            A list of strings representing the prize block.
            
    Returns:
        An list of ints or None (by default).
    """
    if len(block) > 1:
        return [int(num_str) for num_str in block[1].split()]

def parse_given_block(block):
    """ Parses a list of strings into tuples. The tuples are in the format
        (key: int, value: string). 

        E.g. ['9=a', ...]

    Args:
        block:
            A list of strings representing the given block.
            
    Returns:
        A list of tuples(key, value)
    """
    tmp = []

    for given in block:
        if given[0] == '#':
            continue
        else:
            l = given.split('=')
            number, letter = int(l[0].strip()), l[1].strip().upper()
            tmp.append((number, letter))

    return tmp

def parse_guess_block(block):
    """ Parses a list of strings into tuples. The tuples are in the format
        (key: int, value: string). 

        E.g. ['9=a', ...]

        Sometimes no clues can be loaded.

    Args:
        block:
            A list of strings representing the guess block.
            
    Returns:
        An list of tuples(key, value)
    """
    tmp = []

    for guess in block:
        if guess[0] == '#':
            continue
        else:
            l = guess.split('=')
            
            number, letter = int(l[0].strip()), l[1].strip().upper()
            tmp.append((number, letter))

    return tmp

def parse_grid_block(block, x=15, y=15):
    """ Parses a list of strings into lists of integers, these are the rows in
        the grid which are then loaded into a numpy array. 

        E.g. '25 0 0 9 16 19 24 0 2 15 20 17 0 0 1' 
    Args:
        block:
            A list of strings representing the grid block.
            
    Raises:
        BreakerParseError:
            To help locate probems when inputting a line in the 15x15 grid.

    Returns:
        A numpy array
    """
    grid_array = []

    for i, line in enumerate(block):
        if line[0] == '#' or line[0] =='':
            continue

        values = line.split()
        grid_array.append([int(num_str) for num_str in line.split()])
        
        if len(values) != y:
            raise BreakerParseError(f'Incorrect line input in grid. Line {i} length {len(values)}')

    return np.array(grid_array)