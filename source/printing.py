import string

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

def pretty_print_grid(cashbreaker):
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

def pretty_print_cashbreaker(cb):
    pretty_print_prize_code(cb)  
    pretty_print_unused_letters(cb)
    pretty_print_code(cb)
    pretty_print_grid(cb)

#endregion