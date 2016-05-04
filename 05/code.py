import telnetlib
import string
from collections import Counter


def read():
    ind, mat, txt = t.expect(["> ", "Press enter to continue..."], 2)
    return txt, ind == 0

def get_word(v):
    word = v.split('\n')[-3].strip().replace(' ','')
    return word

def get_char_in_word(word, char):
    return [i for i in xrange(len(word)) if word[i] == char]

def most_common_char(words, space_char):
    ct = Counter()
    for word in words:
        w = set([word[i] for i in space_char])
        for c in w:
            ct[c] += 1
    return ct.most_common(1)[0][0]

def play_game(hangword):
    valid_words = words_by_len[len(hangword)][:]
    space_char = get_char_in_word(hangword, '_')
    while True:
        char = most_common_char(valid_words, space_char)
        print char
        t.write(char)
        v, playing = read()
        print v
        if not playing:
            t.write('\n')
            return  
        hangword = get_word(v)
        found_char = get_char_in_word(hangword, char)
        space_char = get_char_in_word(hangword, '_')
        print space_char
        next_words = []
        rem_chars = set([])
        for word in valid_words:
            if get_char_in_word(word, char) == found_char:
                next_words.append(word)
        valid_words = next_words
        print valid_words

words = open("words.txt").readlines()
words_by_len = [[] for i in xrange(50)]
for word in words:
    words_by_len[len(word.strip())].append(word.strip())

t = telnetlib.Telnet("52.49.91.111", 9988)
v = t.read_until("Press enter to continue...")
print v
t.write("\n")
while True:
    v, playing = read()
    print v
    hangword = get_word(v)
    play_game(hangword)
