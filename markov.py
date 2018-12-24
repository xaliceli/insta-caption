"""
generate.py
Generates captions using Markov chains.
Corpus created using scrape.py.
"""

import random

import numpy as np

class MarkovText():
    """
    Generates text using Markov chains.
    """

    def __init__(self, file):
        self.corpus = None
        self.dict = {}
        self.read_corpus(file)

    def read_corpus(self, file):
        """
        Reads in text file to serve as corpus.
        Splits text into individual words.
        """
        text = open(file, encoding='utf8').read()
        corpus = text.split()
        self.corpus = corpus

    def init_pairs(self):
        """
        Yields all sequential two-word pairs from corpus.
        """
        for i in range(len(self.corpus)-1):
            yield (self.corpus[i], self.corpus[i+1])

    def init_dictionary(self):
        """
        Initializes dictionary with pairs of words.
        """
        pairs = self.init_pairs()
        for word_1, word_2 in pairs:
            if word_1 in self.dict.keys():
                self.dict[word_1].append(word_2)
            else:
                self.dict[word_1] = [word_2]

    def gen_text(self, poss_length=(1, 40)):
        """
        Generates Markov text of length between range.
        """
        start = np.random.choice(self.corpus)
        sentence = [start]
        sentence_length = random.randint(poss_length[0], poss_length[1])
        while len(sentence) < sentence_length:
            sentence.append(np.random.choice(self.dict[sentence[-1]]))
        return ' '.join(sentence)
