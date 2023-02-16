# https://www.crosswordsolver.org

# To run from command prompt
#   type 'cmd' in search box in win 10
#   path in quotes "C:\Users\Craig\Google Drive\Programming & Tech\Python\Python Experiments\Cashbreaker"
#   python cashbreaker.py
#
#   cd "C:\Users\Craig\Google Drive\Programming & Tech\Python\Python Experiments\Cashbreaker"
#   python cashbreaker.py

import os
import string 
import numpy as np
from enum import Enum

import en_words
from breaker_parser import parse_prize_block, parse_given_block, parse_guess_block, parse_grid_block


def array_split(sequence, seperators=[0]):
    chunk = []
    for val in sequence:
        if val in seperators:
            yield chunk
            chunk = []
        else:
            chunk.append(val)
    yield chunk

class BlockType(Enum):
    (Comment, Prize, Given, Guess, Grid) = range(5)

class Cashbreaker():
    def __init__(self):
        self.filename = None
        self.prize_word = None
        self.code_dict = None
        self.given_tuple_list = None
        self.grid = None        

        self.reset_code_dict()

    @classmethod
    def from_file(self, filename):
        cb = Cashbreaker()
        cb.filename = filename

        # region I/O
        with open(filename, 'r') as f:
            content = f.read()
            blocks = content.split('\n\n')
            
            # Prize
            block = blocks[BlockType.Prize.value].split('\n')
            cb.prize_word = parse_prize_block(block) 
                
            # Given
            block = blocks[2].split('\n')
            cb.given_tuple_list = parse_given_block(block)

            cb.reset_code_dict() # TODO why here? befor gueesses

            # Guess
            block = blocks[3].split('\n')
            for k, v in parse_guess_block(block):
                cb.code_dict[k] = v

            # Grid
            block = blocks[4].split('\n')
            cb.grid = parse_grid_block(block)

            self.numeric_words = cb.find_numeric_words()

        return cb

    #region properties

    @property
    def code_dict_letters(self):
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
                            if letter not in self.code_dict_letters])

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
        numeric_words = []

        # Loop through rows and columns at the same time
        for line in [*self.grid, *self.grid.T]:
            for word in array_split(line):
                if len(word) > 2:
                    numeric_words.append(word)

        return numeric_words       

    def find_valid_words(self, unknown_word):
        result = en_words.potential_words(unknown_word)

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
            potential_letters = [word[i] for i, x in enumerate(unknown_word) if x in en_words.MISSING_CHARACTERS]
            
            # Only accept words that have no missing letters in the dict.
            if any(letter.upper() in self.code_dict_letters for letter in potential_letters):
                continue
            else:
                potential_words.append(word)

        return potential_words


    def guess(self):
        ''' Try to guess words '''
        # No words to find
        if self.is_complete:
            return False

        words_found = False
  
        for numeric_word in self.find_numeric_words():
            alpha_word = [self.code_dict[letter] for letter in numeric_word]

            # Already solved
            if '_' not in alpha_word:
                continue

            # Get all potential matches
            result = en_words.potential_words(''.join(alpha_word)) 
 
            # For each potential match, only allow words with letters not in the code_dict
            # result = [word for word in result if any(letter not in self.code_dict.values() for letter in word.upper())]
            alpha_word = ''.join(alpha_word)
            result = self.find_valid_words(alpha_word)



            # Success!
            if len(result) == 1:
                words_found = True
                
                # Update all letters in the dict
                # TODO only update missing letters?
                for i, code in enumerate(numeric_word):
                    self.code_dict[code] = result[0][i].upper()                     

                self.guess()

        return words_found

    def all_guesses(self, limit=10):
        ''' Try to guess words '''
        # No words to find
        if self.is_complete:
            return False

        words = []
  
        for numeric_word in self.find_numeric_words():
            alpha_word = [self.code_dict[letter] for letter in numeric_word]

            # Already solved
            if '_' not in alpha_word:
                continue

            # Get all potential matches
            # result = en_words.potential_words(''.join(alpha_word)) 
            # result = [word for word in result if any(letter not in self.code_dict.values() for letter in word.upper())]

            alpha_word = ''.join(alpha_word)
            result = self.find_valid_words(alpha_word)

            # result = self.find_valid_words(unknown_word)

            if len(result) > limit:
                result = result[0:limit] + ["..."]
            
            words.append([alpha_word] + result)
            # words.(result[1:limit+1])


        return words






    def reset_code_dict(self):
        self.code_dict = dict.fromkeys(range(1, 26+1), "_")
        self.code_dict[0] = '■' 

        if self.given_tuple_list != None:
            for item in self.given_tuple_list:
                self.code_dict[item[0]] = item[1]


    def get_grid_number(self, x, y):
        inverted_shape = self.grid.shape[::-1]

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
            e.g. 'Cashbreaker('001.txt', (15, 15), 'WAY', Incomplete)'

        Args:
            None.

        Returns:
            A string representing the cashbreaker.
        """
        breaker_name = os.path.basename(self.filename)
        status = 'Complete' if self.is_complete else 'Incomplete'
        
        return f'Cashbreaker({breaker_name}, {self.grid.T.shape}, {self.code_dict_letters}, {status})'
        
 








 


 
 