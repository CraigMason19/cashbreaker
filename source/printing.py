import string

# region pretty printing

def print_prize_code(cashbreaker):
    """ Prints the prize code in a nicer way in the terminal. E.g.

        Prize:
        20 13  1 23 4  6
        P  L  A  N  E  T

    Args:
        cashbreaker:
            A Cashbreaker Class.
            
    Returns:
        None.
    """
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

def print_unused_letters(cashbreaker):
    """ Prints the unused letters in a nicer way in the terminal. E.g.

        Unused letters:
            A B C D E F G ...

    Args:
        cashbreaker:
            A Cashbreaker Class.
            
    Returns:
        None.
    """
    print("Unused letters:")

    if len(cashbreaker.unused_letters) == 0:
        print("  N/A")
    else:
        print(f"  {' '.join(cashbreaker.unused_letters)}")
    
    print("")

def print_code(cashbreaker):
    """ Prints the code dict in a nicer way in the terminal. E.g.

        Code Table:
        1  2  3  4  5  6  7  8  9 10 11 12 13
        V  T  A  H  N  G  O  B  S  K  U  P  D

        14 15 16 17 18 19 20 21 22 23 24 25 26
        Y  W  J  X  E  Q  Z  L  M  F  R  I  C

    Args:
        cashbreaker:
            A Cashbreaker Class.
            
    Returns:
        None.
    """
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

def print_grid(cashbreaker):
    """ Prints the grid in a nicer way in the terminal. 
    
        Prints the grid with numbers on the side and on the top.

    Args:
        cashbreaker:
            A Cashbreaker Class.
            
    Returns:
        None.
    """
    x, y = cashbreaker.grid.shape

    table_data = [
        [""] + [f"{i:02d}" for i in range(1, x+1)], # plus 1 because there is a row in front
        [" "] + ["___" for i in range(1, x+1)],
    ]

    for i, l in enumerate(cashbreaker.grid):
        table_data.append([f"{i+1:02d}|"] + [str(cashbreaker.code_dict[num]) for num in l])

    print("Grid:")

    for row in table_data:
        print(("{: >3}" * (x+1)).format(*row))

    print("")

def print_cashbreaker(cashbreaker):
    print_prize_code(cashbreaker)  
    print_unused_letters(cashbreaker)
    print_code(cashbreaker)
    print_grid(cashbreaker)

#endregion