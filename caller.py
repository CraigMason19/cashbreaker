import os 
import pathlib
import string

import numpy as np

from cashbreaker import Cashbreaker
from printing import print_cashbreaker

def main():
    breaker_name = "001.txt"
    project_path = str(pathlib.Path(__file__).parent)
    cb = Cashbreaker.from_file(project_path + "\\breakers\\" + breaker_name)

    redraw = True
 
    exit_strings = ["close", "c", "exit", "e"]
    clear_strings = ["cls", "clear"]
    reset_strings = ["reset", "r"]
    help_strings = ["help", 'h']
    guess_strings = ["guess", "g", "fill", 'f']
    reload_strings = ["reload"]
    repr_strings = ["repr"]

    while True:
        if redraw:
            os.system('cls')
            print_cashbreaker(cb)

        # Process input 
        readline = input().lower()

        if readline in exit_strings:
            break
        
        elif readline in clear_strings:
            redraw = True

        elif readline in reload_strings:
            cb = Cashbreaker.from_file(project_path + "\\breakers\\" + breaker_name)
            redraw = True

        elif readline in help_strings:
            print(f"  Assign letter to number -> (number)=(letter)")
            print(f"  Assign letter to location -> (x),(y)=(letter)")
            print("")
            print(f"  Exit -> {exit_strings}")
            print(f"  Clear screen -> {clear_strings}")
            print(f"  Reset -> {reset_strings}")
            print(f"  Close -> {exit_strings}")
            print(f"  Guess words -> {guess_strings}")
            print(f"  Reload -> {reload_strings}")
            print(f"  Show representation -> {repr_strings}")
            print("\n")
            redraw = False

        elif readline in guess_strings:
            if cb.is_complete:
                print("Cashbreaker is complete!\n")
                redraw = False
            else:
                if(cb.guess()):
                    redraw = True
                else:
                    print("No definite answers found\n")
                    redraw = False

        elif readline in repr_strings:
            print(f'__repr__ == {cb}\n')
            redraw = False

        elif readline in reset_strings:
            cb.reset_code_dict()
            redraw = True
    
        else:
            try:
                readline = readline.split('=')

                number = 0
                letter = readline[1].upper()
                parse_success = True

                # e.g. 1,1=s
                if ',' in readline[0]:
                    loc = [int(index) for index in readline[0].split(',')]

                    try:
                        number = cb.get_grid_number(loc[0], loc[1])

                    except IndexError as e:
                        print(str(e) + "\n")
                        parse_success = False
                        redraw = False

                # e.g. 1=g
                else:
                    number = int(readline[0])

                if(parse_success):
                    # Only add valid characters
                    if letter in (string.ascii_uppercase + "_"):
                        if number == 0:
                            print("Can't assign to empty space\n")
                            redraw = False

                        elif letter != "_" and letter in cb.code_dict_letters:
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