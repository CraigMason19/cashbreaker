import numpy as np

class BreakerParseError(Exception):
    pass

def parse_prize_block(prize_block):
    ''' return none by default '''
    if len(prize_block) > 1:
        return [int(num_str) for num_str in prize_block[1].split()]

def parse_guess_block(guess_block):
    tmp = []

    for guess in guess_block:
        if guess[0] == '#':
            continue
        else:
            l = guess.split('=')
            
            number, letter = int(l[0].strip()), l[1].strip().upper()
            tmp.append(key, value)

    return tmp

def parse_grid_block(grid_block, x=15, y=15):
    grid_array = []

    for i, line in enumerate(grid_block):
        if line[0] == '#' or line[0] =='':
            continue

        values = line.split()
        grid_array.append([int(num_str) for num_str in line.split()])
        
        if len(values) != y:
            raise BreakerParseError(f'Incorrect line input in grid. Line {i} length {len(values)}')

    return np.array(grid_array)