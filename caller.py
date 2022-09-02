import os 
import pathlib
import string

from cashbreaker import Cashbreaker



# region pretty printing
def pretty_print_prize_code(cashbreaker):
    print("Prize:")

    if cashbreaker.prize_word == None:
        print("  N/A")
    else:
        table_data = [
            cashbreaker.prize_word,
            [str(cashbreaker.code_dict[num]) for num in cashbreaker.prize_word]
        ]

        for row in table_data:
            print(("{: >3}" * (len(cashbreaker.prize_word))).format(*row))

    print("")

def pretty_print_unused_letters(cashbreaker):
        unused = string.ascii_uppercase
        x = ' '.join([letter for letter in unused if letter not in cashbreaker.code_dict.values()])
        
        print("Unused letters:")

        if len(x) == 0:
            print("  N/A")
        else:
            print(f"  {x}")
        
        print("")

def pretty_print_code(cashbreaker):
    key_list = list(cashbreaker.code_dict.keys())
    value_list = [str(v) for v in cashbreaker.code_dict.values()]

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

def pretty_print_grid(cashbreaker, grid_width=15):
    table_data = [
        [""] + [f"{i:02d}" for i in range(1, grid_width+1)], # plus 1 for last number = 1 for extra colum for row num
        [" "] + ["___" for i in range(1, grid_width+1)],
    ]

    for i, l in enumerate(cashbreaker.grid):
        table_data.append([f"{i+1:02d}|"] + [str(cashbreaker.code_dict[num]) for num in l])

    print("Grid:")

    for row in table_data:
        print(("{: >3}" * (grid_width+1)).format(*row))

    print("")
#endregion




def main():
    project_path = str(pathlib.Path(__file__).parent)
    cb = Cashbreaker.from_file(project_path + "\\breakers\\" + "003.txt")

    redraw = True
 
    exit_strings = ["close", "c", "exit", "e"]
    clear_strings = ["cls", "clear"]
    reset_strings = ["reset", "r"]
    help_strings = ["help", 'h']
    guess_strings = ["guess", "g"]

    while True:
        if redraw:
            os.system('cls')
            pretty_print_prize_code(cb)
            pretty_print_unused_letters(cb)
            pretty_print_code(cb)
            pretty_print_grid(cb)



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

        elif readline in guess_strings:
            cb.guess()
            redraw = True


        elif readline in reset_strings:
            cb.reset_code_dict()
            redraw = True
    
        else:
            try:
                readline = readline.split('=')

                number = 0
                letter = readline[1].upper()

                #1,1=s
                if ',' in readline[0]:
                    grid_ref = readline[0].split(',')
                    number = cb.get_grid_number(int(grid_ref[0]), int(grid_ref[1]))
                else:
                    number = int(readline[0])


                # Only add valid characters
                if letter in (string.ascii_uppercase + "_"):
                    if number == 0:
                        print("Can't assign to empty space\n")
                        redraw = False

                    elif letter != "_" and letter in cb.code_dict.values():
                        print("Letter already in use, please unassign it first '_'\n")
                        redraw = False
                    else:
                        cb.code_dict[number] = letter
                        redraw = True
                else:
                    print("Letter not valid. Please us a-z, A-Z or '_'\n")
                    redraw = False

            except:
                print("Unrecognized input, type 'help' for more info\n")
                redraw = False


if __name__ == "__main__":
    main()