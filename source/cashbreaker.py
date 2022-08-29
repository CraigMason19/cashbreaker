# https://www.crosswordsolver.org

# To run from command prompt
#   type 'cmd' in search box in win 10
#   path in quotes "C:\Users\Craig\Google Drive\Programming & Tech\Python\Python Experiments\Cashbreaker"
#   python cashbreaker.py
#
#   cd "C:\Users\Craig\Google Drive\Programming & Tech\Python\Python Experiments\Cashbreaker"
#   python cashbreaker.py

import os 
import pathlib
import string



class Cashbreaker():
    def __init__(self, filename):
        self.filename = filename
        pass

    def create_from_file():
        pass

    def save_guesses(self):
        pass

    def reload(self):
        pass

    def reset(self):
        pass 





    def __str__(self):
        pass

    def __repr__(self):
        pass
 

def init_dict(tuple_list):
    cd = dict.fromkeys(range(1, 26+1), "_")
    cd[0] = '■' 

    # Initial
    for item in tuple_list:
        cd[item[0]] = item[1]

    return cd

CODE_DICT = None
PRIZE_WORD = None
GRID = []
GIVEN_TUPLE_LIST = []
cashbreaker_name = '003.txt' 


project_path = str(pathlib.Path(__file__).parent.parent)

 
# region I/O
with open(project_path + "/breakers/" + cashbreaker_name, 'r') as f:
    content = f.read()
    blocks = content.split('\n\n')
    
    # Prize
    prize_block = blocks[1].split('\n')
    if len(prize_block) > 1:
        PRIZE_WORD = [int(num_str) for num_str in prize_block[1].split()]
        
    # Given
    given_block = blocks[2].split('\n')
    for given in given_block:
        if given[0] == '#':
            continue
        else:
            l = given.split('=')
            number, letter = int(l[0].strip()), l[1].strip().upper()
            GIVEN_TUPLE_LIST.append((number, letter))

    CODE_DICT = init_dict(GIVEN_TUPLE_LIST)



    # Guess
    guess_block = blocks[3].split('\n')
    for guess in guess_block:
        if guess[0] == '#':
            continue
        else:
            l = guess.split('=')
            
            number, letter = int(l[0].strip()), l[1].strip().upper()
            CODE_DICT[number] = letter

    # Grid
    grid_block = blocks[4].split('\n')
    for line in grid_block:
        if line[0] == '#' or line[0] =='':
            continue
        else:
            GRID.append([int(num_str) for num_str in line.split()])
#endregion

 
 

# region pretty printing
def pretty_print_prize_code():
    global PRIZE_WORD

    print("Prize:")

    if PRIZE_WORD == None:
        print("  N/A")
    else:
        table_data = [
            PRIZE_WORD,
            [str(CODE_DICT[num]) for num in PRIZE_WORD]
        ]

        for row in table_data:
            print(("{: >3}" * (len(PRIZE_WORD))).format(*row))

    print("")

def pretty_print_unused_letters():
        unused = string.ascii_uppercase
        x = ' '.join([letter for letter in unused if letter not in CODE_DICT.values()])
        
        print("Unused letters:")

        if len(x) == 0:
            print("  N/A")
        else:
            print(f"  {x}")
        
        print("")

def pretty_print_code():
    key_list = list(CODE_DICT.keys())
    value_list = [str(v) for v in CODE_DICT.values()]

    table_data = [
        key_list[0:13],
        value_list[0:13],

        ["" for i in range(1, 13+1)],

        key_list[13:],
        value_list[13:],
    ]

    print("Code Table:")

    for row in table_data:
        print(("{: >3}" * 13).format(*row))

    print("")

def pretty_print_grid(grid_width=15):
    global GRID

    table_data = [
        [""] + [f"{i:02d}" for i in range(1, grid_width+1)], # plus 1 for last number = 1 for extra colum for row num
        [" "] + ["___" for i in range(1, grid_width+1)],
    ]

    for i, l in enumerate(GRID):
        table_data.append([f"{i+1:02d}|"] + [str(CODE_DICT[num]) for num in l])

    print("Grid:")

    for row in table_data:
        print(("{: >3}" * (grid_width+1)).format(*row))

    print("")
#endregion




def main():
    global CODE_DICT
    global GIVEN_TUPLE_LIST

    redraw = True
 
    exit_strings = ["close", "c", "exit", "e"]
    clear_strings = ["cls", "clear"]
    reset_strings = ["reset", "r"]
    help_strings = ["help", 'h']

    while True:
        if redraw:
            os.system('cls')
            pretty_print_prize_code()
            pretty_print_unused_letters()
            pretty_print_code()
            pretty_print_grid()



        # Process input 
        readline = input().lower()

        if readline in exit_strings:
            break
        
        if readline in clear_strings:
            redraw = True

        elif readline in help_strings:
            print(f"  Assign letter to number -> (number)=(letter)")
            print(f"  Clear screen -> {clear_strings}")
            print(f"  Reset -> {reset_strings}")
            print(f"  Close -> {exit_strings}\n")
            redraw = False

        elif readline in reset_strings:
            CODE_DICT = init_dict(GIVEN_TUPLE_LIST)
            redraw = True
    
        else:
            try:
                readline = readline.split('=')
                number, letter = int(readline[0]), readline[1].upper()

                # Only add valid characters
                if letter in (string.ascii_uppercase + "_"):
                    if letter != "_" and letter in CODE_DICT.values():
                        print("Letter already in use, please unassign it first '_'\n")
                        redraw = False
                    else:
                        CODE_DICT[number] = letter
                        redraw = True
                else:
                    print("Letter not valid. Please us a-z, A-Z or '_'\n")
                    redraw = False

            except:
                print("Unrecognized input, type 'help' for more info\n")
                redraw = False


if __name__ == "__main__":
    main()