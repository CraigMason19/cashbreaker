import os 
import pathlib
import string

import numpy as np

from cashbreaker import Cashbreaker
from printing import pretty_print_cashbreaker

def main():
    breaker_name = "001.txt"
    project_path = str(pathlib.Path(__file__).parent)
    cb = Cashbreaker.from_file(project_path + "\\breakers\\" + breaker_name)

    redraw = True
 
    exit_strings = ["close", "c", "exit", "e"]
    clear_strings = ["cls", "clear"]
    reset_strings = ["reset", "r"]
    help_strings = ["help", 'h']
    guess_strings = ["guess", "g"]
    reload_strings = ["reload"]

    while True:
        if redraw:
            os.system('cls')
            pretty_print_cashbreaker(cb)

        # Process input 
        readline = input().lower()

        if readline in exit_strings:
            break
        
        if readline in clear_strings:
            redraw = True

        if readline in reload_strings:
            cb = Cashbreaker.from_file(project_path + "\\breakers\\" + breaker_name)
            redraw = True

        elif readline in help_strings:
            print(f"  Assign letter to number -> (number)=(letter)")
            print(f"  Clear screen -> {clear_strings}")
            print(f"  Reset -> {reset_strings}")
            print(f"  Close -> {exit_strings}\n")
            redraw = False

        elif readline in guess_strings:
            if cb.is_complete():
                print("Cashbreaker is complete!\n")
                redraw = False
            else:
                if(cb.guess()):
                    redraw = True
                else:
                    print("No definite answers found\n")
                    redraw = False




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
                    grid_ref = [int(index) for index in readline[0].split(',')]

                    # check in range
                    if 0 <= grid_ref[0] <= cb.grid.shape[0]:
                        if 0 <= grid_ref[1] <= cb.grid.shape[1]:
                            number = cb.get_grid_number(grid_ref[0], grid_ref[1])
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