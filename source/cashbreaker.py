# https://www.crosswordsolver.org

# To run from command prompt
#   type 'cmd' in search box in win 10
#   path in quotes "C:\Users\Craig\Google Drive\Programming & Tech\Python\Python Experiments\Cashbreaker"
#   python cashbreaker.py
#
#   cd "C:\Users\Craig\Google Drive\Programming & Tech\Python\Python Experiments\Cashbreaker"
#   python cashbreaker.py

 
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

        return cb

    def is_complete(self):
        return '_' not in self.code_dict.values()

    def save_guesses(self):
        pass

    def reload(self):
        pass

    def find_words_gen(self):
        for line in self.grid:
            for word in array_split(line):
                if len(word) < 2:
                    continue
                else:
                    yield word

        for line in self.grid.T:
            for word in array_split(line):
                if len(word) < 2:
                    continue
                else:
                    yield word
                    # yield ''.join([self.code_dict[letter] for letter in word])

    def guess(self):
 
        # No words to find
        if self.is_complete():
            return False


        words_found = False
 

 
        x = self.find_words_gen()
        # go through all words
        # check if there is only one option for word
 
        for word in x:
            # tmp = # MAKE WORK ???????
            # if en_words.potential_words(word)
            
            alpha_word = [self.code_dict[letter] for letter in word]

            # Already solved
            if '_' not in alpha_word:
                continue

            result = en_words.potential_words(''.join(alpha_word)) 
            # if missing letter already in dict
            # gazelle, #gabelle

            # Success!
            if len(result) == 1:
                # print(result[0])
                 
                for i, code in enumerate(word):
                    self.code_dict[code] = result[0][i].upper()
                    words_found = True

                self.guess()

        # print("no more matches")
        a=10
        ## if not return string (no certain guesses)

        return words_found


    def reset_code_dict(self):
        self.code_dict = dict.fromkeys(range(1, 26+1), "_")
        self.code_dict[0] = '■' 

        if self.given_tuple_list != None:
            for item in self.given_tuple_list:
                self.code_dict[item[0]] = item[1]

    def get_grid_number(self, x, y):
        x = self.grid[x-1][y-1]
        return int(x)


    def __str__(self):
        pass

    def __repr__(self):
        pass
 








 


 
 