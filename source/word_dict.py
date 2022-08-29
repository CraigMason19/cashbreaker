import os

path_name = os.path.dirname(__file__)
dict_name = 'en_dic'

filename = path_name + '/' + dict_name + '.txt'
filename_sorted = path_name + '/' + dict_name + '_sorted.txt'


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
    def match(a, b):
        for letter_a, letter_b in zip(a, b):
            if letter_a == '?':
                continue
            elif letter_a != letter_b:
                return False

        return True

    with open(filename_sorted) as f:

        letter_count = 0
        length = len(word)
        words = []

        while letter_count <= length:
            line = f.readline().strip().lower()
            letter_count = len(line)

            if letter_count == length:
                if match(word.lower(), line):
                    words.append(line)
                else:
                    continue

        return words




w = words_of_length(4)
# print(w)

pw = potential_words("?azelle")
print(pw)