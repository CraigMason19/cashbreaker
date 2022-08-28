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




 
 

def init_dict(tuple_list):
    cd = dict.fromkeys(range(1, 26+1), "_")
    cd[0] = '■' 

    # Initial
    for item in tuple_list:
        cd[item[0]] = item[1]
    # # Initial
    # cd[2] = 'A'
    # cd[9] = 'G'
    # cd[24] = 'N'

    return cd

CODE_DICT = None
PRIZE_WORD = None
GRID = []
GIVEN_TUPLE_LIST = []
cashbreaker_name = '002.txt' 
file_path = str(pathlib.Path(__file__).parent)


# region I/O
with open(file_path + "/breakers/" + cashbreaker_name, 'r') as f:
    content = f.read()
    blocks = content.split('\n\n')
    
    # Prize
    prize_block = blocks[1].split('\n')
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

 

# grid = [
#     # ['', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
#     # [],
#     [3, 2, 18, 3, 25, 25, 0, 1, 0, 21, 22, 19, 1, 23, 17],
#     [26, 0, 2, 0, 0, 15, 19, 26, 2, 22, 0, 0, 25, 0, 8],
#     [25, 16, 24, 2, 14, 17, 0, 25, 0, 19, 18, 15, 25, 16, 14],
#     [20, 0, 0, 9, 0, 24, 0, 6, 0, 11, 0, 25, 0, 0, 16],
#     [20,19,26,25,0,0,19,24,24,0,0,20,25,10,2],
#     [25,0,0,9,16,19,24,0,2,15,20,17,0,0,1],
#     [18,25,6,0,2,0,12,17,9,0,15,0,13,25,14],
#     [0,0,16,22,3,7,0,16,0,11,17,16,25,0,0],
#     [1,25,7,0,3,0,9,2,20,0,26,0,3,22,24],
#     [2,0,0,5,19,20,2,0,23,2,26,10,0,0,25],
#     [24,25,4,17,0,0,15,2,7,0,0,26,7,24,8],
#     [5,0,0,19,0,13,0,6,0,17,0,2,0,0,19],
#     [2,9,17,24,4,2,0,2,0,15,25,14,2,14,25],
#     [20,0,18,0,0,1,25,16,9,19,0,0,16,0,22],
#     [20,21,22,2,6,12,0,4,0,1,25,20,18,25,20],

# ]

 

# region pretty printing
def pretty_print_prize_code():
    global PRIZE_WORD

    print("Prize:")

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