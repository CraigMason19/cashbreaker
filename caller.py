#-------------------------------------------------------------------------------
# Name:        caller.py
#
# Notes:       A console application to interact with a cashbreaker file in the
#              breakers folder. 
#
# Links:        
#
# TODO:        
#
#-------------------------------------------------------------------------------

import os # For cls 
import pathlib
import traceback
import string

from cashbreaker import Cashbreaker
from printing import print_cashbreaker

def main():
    breaker_name = "009.txt"
    project_path = str(pathlib.Path(__file__).parent)

    try:
        cb = Cashbreaker.from_file(project_path + "\\breakers\\" + breaker_name)
    except Exception:
        traceback.print_exc()
        return

    redraw = True
 
    exit_strings = ["close", "c", "exit", "e"]
    clear_strings = ["cls", "clear"]
    reset_strings = ["reset", "r"]
    repr_strings = ["repr"]
    help_strings = ["help", 'h']
    guess_strings = ["guess", "g", "fill", 'f', 'solve', 's']
    all_strings = ['all', 'a']
    all_order_strings = [ 'all order', 'ao']

    while True:
        if redraw:
            os.system('cls')
            print_cashbreaker(cb)

        # Process input 
        readline = input().lower()

        #region Commands
        
        if readline in exit_strings:
            break
        
        elif readline in clear_strings:
            redraw = True

        elif readline in reset_strings:
            cb.reset_code_dict()
            redraw = True

        elif readline in repr_strings:
            print(f'__repr__ == {cb}\n')
            redraw = False

        elif readline in help_strings:
            print(f"  Assign letter to number -> (number)=(letter)")
            print(f"  Assign letter to location -> (x),(y)=(letter)")
            print(f"  Show potentials for a word -> w=(word)")
            print("")
            print(f"  Exit -> {exit_strings}")
            print(f"  Clear screen -> {clear_strings}")
            print(f"  Reset -> {reset_strings}")
            print(f"  Show representation -> {repr_strings}")
            print(f"  Guess words -> {guess_strings}")
            print(f"  Display all words -> {all_strings}")
            print(f"  Display all words ordered by matches -> {all_order_strings}")

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

        # List all potential answers
        elif readline in all_strings + all_order_strings:
            if cb.is_complete:
                print("Cashbreaker is complete!\n")
            else:
                all_potentials = cb.all_potentials()
                total_potentials = 0

                if readline in all_order_strings:
                    all_potentials.sort(key=len)


                for guess in all_potentials:
                    length_of_potentials = len(guess[1:])
                    total_potentials += length_of_potentials

                    print(f'{guess[0]} ({length_of_potentials} potentials)')

                    if length_of_potentials > 10:
                        print(f"\t{guess[1:10+1]}...\n")
                    else:
                        print(f"\t{guess[1:]}\n")

                print(f"{total_potentials} total potentials\n")

            redraw = False

        #endregion

        #region User input 

        else:
            try:
                readline = [_.strip() for _ in readline.split('=')]

                # e.g. w=c?osmos
                if readline[0] == 'w':
                    if not cb.is_complete:
                        result = cb.find_valid_words(readline[1])

                        if not result:
                            print("No words could be found\n")
                        else:
                            print(result)
                            print('\n')
                    else:
                        print("Cashbreaker is complete!\n")

                    redraw = False

                # Letter assignment
                else:
                    number = 0
                    letter = readline[1].upper()
                    parse_success = True

                    # e.g. 1,1=s
                    if ',' in readline[0]:
                        coords = [int(index) for index in readline[0].split(',')]

                        try:
                            number = cb.get_grid_number(*coords)

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

                            elif letter != "_" and letter in cb.used_letters:
                                print("Letter already in use, please unassign it first '_'\n")
                                redraw = False
                            else:
                                cb.assign(number, letter)  
                                redraw = True
                        else:
                            print("Letter not valid. Please us a-z, A-Z or '_'\n")
                            redraw = False

            except:
                print("Unrecognized input, type 'help' for more info\n")
                redraw = False

        #endregion

if __name__ == "__main__":
    main()