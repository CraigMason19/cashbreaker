# https://www.crosswordsolver.org

# To run from command prompt
#   type 'cmd' in search box in win 10
#   path in quotes "C:\Users\Craig\Google Drive\Programming & Tech\Python\Python Experiments\Cashbreaker"
#   python cashbreaker.py
#
#   cd "C:\Users\Craig\Google Drive\Programming & Tech\Python\Python Experiments\Cashbreaker"
#   python cashbreaker.py

 
import string 

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
            prize_block = blocks[1].split('\n')
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
            cb.grid = []

            for line in grid_block:
                if line[0] == '#' or line[0] =='':
                    continue
                else:
                    cb.grid.append([int(num_str) for num_str in line.split()])

        return cb

    def save_guesses(self):
        pass

    def reload(self):
        pass

    def reset_code_dict(self):
        self.code_dict = dict.fromkeys(range(1, 26+1), "_")
        self.code_dict[0] = '■' 

        if self.given_tuple_list != None:
            for item in self.given_tuple_list:
                self.code_dict[item[0]] = item[1]

    def get_grid_number(self, x, y):
        if self.grid == None:
            raise IndexError("Grid has not been set-up")

        return int(self.grid[x-1][y-1])


    def __str__(self):
        pass

    def __repr__(self):
        pass
 








 


 
 