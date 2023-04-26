import os

path_name = os.path.dirname(__file__)
dict_name = 'en_dic'

FILENAME = path_name + '/' + dict_name + '.txt'
FILENAME_SORTED = path_name + '/' + dict_name + '_sorted.txt'

MISSING_CHARACTERS = '?-_.' # guess cahracters e.g. s?a_d -> salad


#region I/O Dictionary
def create_sorted_dict():
    lines = None

    with open(FILENAME) as f:
        lines = f.readlines()
        lines.sort(key=lambda item: (len(item), item))
    
    with open(FILENAME_SORTED, 'w+') as f:
        for line in lines:
            f.write(line)

def word_count_in_dic():
    with open(FILENAME) as f:
        lines = f.readlines()
        return len(lines)
    
def all_unsorted_words():
    with open(FILENAME) as f:
        lines = f.read().lower().splitlines()
        return lines

def all_sorted_words():
    with open(FILENAME_SORTED) as f:
        lines = f.read().lower().splitlines()
        return lines

def words_of_length(length=3):
    if length < 0:
        return []

    with open(FILENAME_SORTED) as f:
        words = []
        letter_count = 0
        
        while letter_count <= length:
            line = f.readline().strip().lower()
            letter_count = len(line)

            if letter_count == length:
                words.append(line)

        return(words)

#endregion

def potential_words(word, ignore_letters='', required_letters=''):
    def is_match(word_a, word_b, ignore_letters='', required_letters=''):
        ''' Compare each letter in each word '''


        for rl in required_letters:
            if rl not in word_b:
                return False

        for letter_a, letter_b in zip(word_a, word_b):
            # Letter in second word is not allowed
            if letter_b in ignore_letters:
                return False

            # Unknown letter, go to the next
            elif letter_a in MISSING_CHARACTERS:
                continue

            # Doesn't fit
            elif letter_a != letter_b:
                return False

        return True

    word = word.lower()
    ignore_letters, required_letters = ignore_letters.lower(), required_letters.lower()

    with open(FILENAME_SORTED) as f:
        letter_count, words = 0, []

        while letter_count <= len(word):
            line = f.readline().strip().lower()
            letter_count = len(line)

            if letter_count == len(word):
                if is_match(word, line, ignore_letters, required_letters):
                    words.append(line)
                else:
                    continue

        return words

def words_from_letters(letters, min_len=3, max_len=6, remove_doubles=False):
    def foo(letters, word, remove_doubles=False):
        if remove_doubles:
            if len(set(word)) != len(word):
                return False

        for letter in word:
            if letter not in letters:
                return False
            
        return True

    letters = letters.lower()    
    l = []

    if max_len == None:
        l = [word for word in all_unsorted_words() if foo(letters, word, remove_doubles)]
        l.sort(key=lambda s: len(s))        

    else:
        for i in range(min_len, max_len+1):
            for word in words_of_length(i):
                if foo(letters, word, remove_doubles):
                    l.append(word)

    return(l)


def main():
    # create_sorted_dict() 

    print(word_count_in_dic()) # 194433

 
    # wol = words_of_length(4)
    # print(wol)


if __name__ == '__main__':
    main()