import random

# 65-90 'A'-'Z' 97-122 'a'-'z'


def generator(lenWord):
    word = ''

    for i in range(0, lenWord):
        r = random.randint(0, 1)
        word = word + chr(random.randint(65, 90) ** r * random.randint(97, 122) ** (1 - r))

    return word

def generatorArrayWords(lenWord, numberWords):
    text = ''

    for i in range(0, numberWords):
        text = text + generator(lenWord) + '\n'

    return text