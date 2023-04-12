import os


def get_words(words: list):
    path = os.path.abspath('./resources/words.txt')
    with open(path) as file:
        for line in file:
            words.append(line.strip())
