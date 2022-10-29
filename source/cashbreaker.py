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
            prize_block = blocks[BlockType.Prize.value].split('\n')
            if len(prize_block) > 1:
                cb.prize_word = [int(num_str) for num_str in prize_block[1].split()]
                
            # Given
            given_block = blocks[2].split('\n')
            cb.given_tuple_list = []

            for given in given_block:
                if given[0] == '#':
                    continue
                else:
                    l = given.split('=')
                    number, letter = int(l[0].strip()), l[1].strip().upper()
                    cb.given_tuple_list.append((number, letter))

            cb.reset_code_dict()

            # Guess
            guess_block = blocks[3].split('\n')
            for guess in guess_block:
                if guess[0] == '#':
                    continue
                else:
                    l = guess.split('=')
                    
                    number, letter = int(l[0].strip()), l[1].strip().upper()
                    cb.code_dict[number] = letter

            # Grid
            grid_block = blocks[4].split('\n')
            grid_array = []

            for line in grid_block:
                if line[0] == '#' or line[0] =='':
                    continue
                else:
                    grid_array.append([int(num_str) for num_str in line.split()])
            
            cb.grid = np.array(grid_array)
            self.numeric_words = cb.find_numeric_words()

        return cb

    #region properties

    @property
    def code_dict_letters(self):
        return ''.join([letter for letter in self.code_dict.values() if letter in string.ascii_uppercase])

    @property
    def unused_letters(self):
        """ Returns a string of all letters not used in the code dictionary.

        Args:
            None.

        Returns:
            A string of all unused letters.
        """
        return ''.join([c for c in string.ascii_uppercase if c not in self.code_dict_letters])

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




    def save_guesses(self):
        pass

    def reload(self):
        pass

    def find_numeric_words(self):
        numeric_words = []

        # Loop through rows and columns at the same time
        for line in [*self.grid, *self.grid.T]:
            for word in array_split(line):
                if len(word) > 2:
                    numeric_words.append(word)

        return numeric_words       

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
 
            # For each potential match, only allow words with letterns not in the code_dict
            result = [word for word in result if any(letter not in self.code_dict.values() for letter in word.upper())]

            # Success!
            if len(result) == 1:
                words_found = True
                
                # Update all letters in the dict
                # TODO only update missing letters?
                for i, code in enumerate(numeric_word):
                    self.code_dict[code] = result[0][i].upper()                     

                self.guess()

        return words_found


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
        
 








 


 
 