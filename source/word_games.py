from en_words import (words_from_letters, potential_words, word_count_in_dic, 
    words_of_length)

def spelling_bee(inner_letter, outer_letters):
    ''' https://spellingbeegame.org '''
    def contains_central_letter(word):
        # return word.find(inner_letter.lower()) == 1
        return (inner_letter.lower() in word)

    letters = outer_letters.lower() + inner_letter.lower()
    
    sb = words_from_letters(letters, min_len=4, max_len=None, remove_doubles=False)
    sb = [word for word in sb if contains_central_letter(word)]

    print(f'Spelling Bee: ({inner_letter.lower()}, {outer_letters.lower()}), count: {len(sb)}')
    print(sb)
    print("")

def wordle():
    ''' https://www.nytimes.com/games/wordle/index.html '''

    word = 'bel?e'
    ignore = 'strncoughxacdwt'
    include = 'el'

    words = potential_words(word, ignore, include)
    print(f'Wordle: {word}, count: {len(words)}')
    print(words)
    print()

def polygon(inner_letter, outer_letters):
    ''' Game from The Times newspaper'''

    def contains_central_letter(word):
        # return word.find(inner_letter.lower()) == 1
        return (inner_letter.lower() in word)

    letters = outer_letters.lower() + inner_letter.lower()
    
    p = words_from_letters(letters, min_len=9, max_len=9, remove_doubles=False)
    p = [word for word in p if contains_central_letter(word)]

    print(f'Polygon: ({inner_letter.lower()}, {outer_letters.lower()})')
    print(p)
    print("")


def cash_square(word_list):
    rows = [w.lower() for w in word_list]
    cols = [''.join(zipped) for zipped in zip(*rows)]

    # recomputes dict 4 times
    col1_words = words_from_letters(cols[0], 4, 4)
    col2_words = words_from_letters(cols[1], 4, 4)
    col3_words = words_from_letters(cols[2], 4, 4)
    col4_words = words_from_letters(cols[3], 4, 4)

    for a in col1_words:
        for b in col2_words:
            for c in col3_words:
                for d in col4_words:
                    row1 = ''.join([a[0], b[0], c[0], d[0]])
                    row2 = ''.join([a[1], b[1], c[1], d[1]])
                    row3 = ''.join([a[2], b[2], c[2], d[2]])
                    row4 = ''.join([a[3], b[3], c[3], d[3]])

                    grid_set = set([row1, row2, row3, row4])

                    if grid_set.issubset(word_list):
                        answer = set(word_list).difference(grid_set)

                        print(f'Cash Grid: ({rows})')
                        
                        for r in [row1, row2, row3, row4]:
                            print(f'\t{" ".join(r).upper()}')

                        print(f'{answer.pop()}')

def main():
    spelling_bee('f', 'eltbad')
    wordle()
    polygon('F', 'lretgure')

    cash_square(['blab', 'ease', 'oils', 'ripe', 'wren'])

if __name__ == '__main__':
    main()