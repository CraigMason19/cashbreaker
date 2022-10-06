import os

path_name = os.path.dirname(__file__)
dict_name = 'en_dic'

filename = path_name + '/' + dict_name + '.txt'
filename_sorted = path_name + '/' + dict_name + '_sorted.txt'

GUESS_CHAACTERS = '?-_.' # guess cahracters e. ?x-

def create_sorted_dict():
    lines = None

    with open(filename) as f:
        lines = f.readlines()
        lines.sort(key=lambda item: (len(item), item))
    
    with open(filename_sorted, 'w+') as f:
        for line in lines:
            f.write(line)

        
def words_of_length(length=3):
    if length < 0:
        return []

    with open(filename_sorted) as f:
        words = []
        letter_count = 0
        
        while letter_count <= length:
            line = f.readline().strip().lower()
            letter_count = len(line)

            if letter_count == length:
                words.append(line)

        return(words)

def potential_words(word):
    def is_match(a, b):
        for letter_a, letter_b in zip(a, b):
            if letter_a in GUESS_CHAACTERS:
                continue
            elif letter_a != letter_b:
                return False

        return True

    word = word.lower()

    with open(filename_sorted) as f:

        letter_count = 0
        length = len(word)
        words = []

        while letter_count <= length:
            line = f.readline().strip().lower()
            letter_count = len(line)

            if letter_count == length:
                if is_match(word, line):
                    words.append(line)
                else:
                    continue

        return words




#w = words_of_length(4)
# print(w)





# add ignor letters as string e..g 'abscl'
# guess cahracters e. ?x-
pw = potential_words("t??ne")
print(pw)