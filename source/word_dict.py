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

#endregion
        
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

def potential_words(word, ignore_letters=''):
    def is_match(word_a, word_b, ignore_letters=''):
        ''' Compare each letter in each word '''

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

    with open(FILENAME_SORTED) as f:
        letter_count, words = 0, []

        while letter_count <= len(word):
            line = f.readline().strip().lower()
            letter_count = len(line)

            if letter_count == len(word):
                if is_match(word, line, ignore_letters):
                    words.append(line)
                else:
                    continue

        return words



def main():
    # create_sorted_dict()
    
    # wol = words_of_length(4)
    # print(wol)

    pw = potential_words("t?ine")
    pw2 = potential_words("t?ine", 'w')
    print(pw)
    print(pw2)

if __name__ == '__main__':
    main()