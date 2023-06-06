#-------------------------------------------------------------------------------
# Name:        cashbreaker.py
#
# Notes:       A class to help me solve the cashbreakers in the UK puzzle 
#              magazines. (Because I hate doing them!)
#
# Links:        
#
# TODO:        
#
#-------------------------------------------------------------------------------

import os
import string 
from enum import Enum

import numpy as np

import en_words as ew
import breaker_parser as bp

def array_split_gen(sequence, seperators=[0]):
    """ A generator that yields an array into sub-arrays.
        E.g. for _ in array_split_gen([2,3,4,5,0,6,7,0,8,9,10,0,11,12], [0]):
                print(_)

                [2, 3, 4, 5]
                [6, 7]    
                [8, 9, 10]
                [11, 12]

    Args:
        sequence:
            The array to be split up.
        seperators:
            An array of seperators to split on.

    Returns:
        A generator.
    """
    chunk = []

    for val in sequence:
        if val in seperators:
            yield chunk
            chunk = []
        else:
            chunk.append(val)

    yield chunk

class BlockType(Enum):
    """ A enum describing the data for loading cashbreakers from a file. 

    Attributes:
        type attributes:
            5 class attributes representing a Enum.
    """
    (Comment, Prize, Given, Guess, Grid) = range(5)

class Cashbreaker():
    """
    
    
    TODO: Implement
    
    
    """
    def __init__(self):
        """ A class representing a cashbreaker found in UK puzzle magazines.

        Args:
            None.

        Returns:
            None.
        """  
        self.filename = None
        self.prize_word = None
        self.code_dict = None
        self.given_tuple_list = None
        self.grid = None        

        self.reset_code_dict()

    @classmethod
    def from_file(self, filename):
        """ A class method to load a cashbreaker from a text file. 

        Args:
            filename:
                The text file to load.

        Returns:
            A Cashbreaker class.
        """
        cb = Cashbreaker()
        cb.filename = filename
        
        with open(filename, 'r') as f:
            content = f.read()
            blocks = content.split('\n\n')
            
            # Prize
            block = blocks[BlockType.Prize.value].split('\n')
            cb.prize_word = bp.parse_prize_block(block) 
                
            # Given
            block = blocks[BlockType.Given.value].split('\n')
            cb.given_tuple_list = bp.parse_given_block(block)

            cb.reset_code_dict() 

            # Guess
            block = blocks[BlockType.Guess.value].split('\n')
            for k, v in bp.parse_guess_block(block):
                cb.code_dict[k] = v

            # Grid
            block = blocks[BlockType.Grid.value].split('\n')
            cb.grid = bp.parse_grid_block(block)

            self.numeric_words = cb.find_numeric_words() 

        return cb

    #region properties

    @property
    def used_letters(self):
        """ Returns a string of all letters that are in the code dictionary.

        Args:
            None.

        Returns:
            A string of all used letters.
        """
        return ''.join([letter for letter in self.code_dict.values() 
                            if letter in string.ascii_uppercase])

    @property
    def unused_letters(self):
        """ Returns a string of all letters not used in the code dictionary.

        Args:
            None.

        Returns:
            A string of all unused letters.
        """
        return ''.join([letter for letter in string.ascii_uppercase 
                            if letter not in self.used_letters])

    @property
    def is_complete(self):
        """ Returns a bool representing if the cashbreaker is complete or not.
        
        Complete is when every key in the code dictionary has a unique letter.

        Args:
            None.

        Returns:
            True if cashbreaker is complete, false otherwise.
        """
        return '_' not in self.code_dict.values()

    #endregion

    def find_numeric_words(self):
        """ Finds a list of all horizontal and vertical words in the breaker. 
            These words will be represented in an list containing their 
            numeric keys in the code dict.
            
            e.g. [[13, 18, 8, 2], [11, 5, 25, 1, 18, 24, 9, 3, 21], ...] 

        Args:
            None.
                
        Returns:
            A list of lists.
        """
        numeric_words = []

        # Loop through rows and columns at the same time
        for line in [*self.grid, *self.grid.T]:
            for word in array_split_gen(line):
                if len(word) > 2:
                    numeric_words.append(word)

        return numeric_words       

    def assign(self, number, letter):
        """ Assigns a letter to a number in the code dict.

        Args:
            number:
                The code dict key.
            letter:
                The code dict value.
                
        Returns:
            None.
        """
        self.code_dict[number] = letter.upper() 














    # For each potential match, only allow words with letters not in the code_dict
    # result = [word for word in result if any(letter not in self.code_dict.values() for letter in word.upper())]
    




    def find_valid_words(self, unknown_word):
        result = ew.potential_words(unknown_word)

        # words not with one option, check if now there is one.
        # why does recipet not go in??
        potential_words = []
        for word in result:
            # Find all guessed letters
            #
            # ??anne?
            # channel
            # chl
            # ignore if chl in dict
            potential_letters = [word[i] for i, x in enumerate(unknown_word) if x in ew.MISSING_CHARACTERS]
            
            # Only accept words that have no missing letters in the dict.
            if any(letter.upper() in self.used_letters for letter in potential_letters):
                continue
            else:
                potential_words.append(word)

        return potential_words












    def _numeric_word_to_string(self, numeric_word):
        return ''.join([self.code_dict[letter] for letter in numeric_word])







    def solve(self):
        """
        """
        if self.is_complete:
            return False

        word_was_found = False
  
        for numeric_word in self.find_numeric_words():
            string_word = self._numeric_word_to_string(numeric_word)

            # Already solved
            if '_' not in string_word:
                continue

            result = self.find_valid_words(string_word)

            # Success!
            if len(result) == 1:
                word_was_found = True
                
                # Update all new letters in the dict
                for i, code in enumerate(numeric_word):
                    if self.code_dict[code] == '_':
                        self.code_dict[code] = result[0][i].upper()                     

                self.solve()

        return word_was_found

















    def all_potentials(self):
        """
        """
        if self.is_complete:
            return False

        words = []
  
        for numeric_word in self.find_numeric_words():
            string_word = self._numeric_word_to_string(numeric_word)

            # Already solved
            if '_' not in string_word:
                continue

            result = self.find_valid_words(string_word)

            words.append([string_word] + result)
    
        return words






















    def reset_code_dict(self):
        """ Creates a blank code dictionary where every letter is '_' 
           (unassigned). Then loads any values that were given in the breaker
            file.

        Args:
            None.
                
        Returns:
            None.
        """
        self.code_dict = dict.fromkeys(range(1, 26+1), "_")
        self.code_dict[0] = '■' 

        # load any values that were given in the breaker file
        if self.given_tuple_list != None:
            for item in self.given_tuple_list:
                self.code_dict[item[0]] = item[1]


    def get_grid_number(self, x, y):
        """ Returns an int representing the grid coordinates value. Will return 
            0 if the grid is a blank space.

        Args:
            x:
                The x coordinate of the cashbreaker (horizontal).
            y:
                The y coordinate of the cashbreaker (vertical).
                
        Raises:
            IndexError:
                If the x or y index is out of bounds.

        Returns:
            An int representing the grid coordinates value.
        """
        inverted_shape = self.grid.shape[::-1] # the transform

        if x < 1 or y < 1:
            raise IndexError(f"Index out of lesser range: {x, y}")
    
        elif x > inverted_shape[0] or y > inverted_shape[1]:
            raise IndexError(f"Index out of greater range: {x, y}")

        # numpy is not 'along the corridor and up the stairs'
        return int(self.grid[y-1, x-1]) 

    def __repr__(self):
        """ Returns a string representing the cashbreaker. 
        
            NOTE: __str__ is not defined so __repr__ wil be used on str methods.

            Returns a string in the format 'Cashbreaker(name, shape, letters, status)
            if it has been loaded.
            e.g. 'Cashbreaker('001.txt', (15, 15), 'WAY', Incomplete)'

            Otherwise returns 'Cashbreaker()' 

        Args:
            None.

        Returns:
            A string representing the cashbreaker.
        """
        if self.filename == None:
            return 'Cashbreaker()'

        breaker_name = os.path.basename(self.filename)
        status = 'Complete' if self.is_complete else 'Incomplete'
        
        return f'Cashbreaker({breaker_name}, {self.grid.T.shape}, {self.used_letters}, {status})'