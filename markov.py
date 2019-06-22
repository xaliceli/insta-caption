"""
generate.py
Generates captions using Markov chains.
Corpus created using scrape.py.
"""

import random
import json
import pandas as pd

class MarkovText():
    """
    Generates text using Markov chains.
    """

    def __init__(self, file, type='json', col=None):
        self.corpus = None
        self.dict = {}
        self.generated = {'captions': []}
        self.read_corpus(file, type, col)

    def read_corpus(self, file, type, col):
        """
        Reads in text file to serve as corpus.
        Splits text into individual words.
        """
        if type == 'json':
            with open(file, 'r') as filehandle:
                text = json.load(filehandle)
        elif type == 'csv':
            df = pd.read_csv(file, delimiter=',')
            text = df[df[col].notnull()][col].tolist()
        self.corpus = [caption.split() for caption in text]

    def init_pairs(self):
        """
        Yields all sequential two-word pairs from corpus.
        """
        for text in self.corpus:
            for i in range(len(text)-1):
                yield (text[i], text[i+1])

    def init_dictionary(self):
        """
        Initializes dictionary with pairs of words.
        """
        pairs = self.init_pairs()
        for word_1, word_2 in pairs:
            if not '@' in word_1 and not '@' in word_2:
                if word_1 in self.dict.keys():
                    self.dict[word_1].append(word_2)
                else:
                    self.dict[word_1] = [word_2]

    def gen_text(self, poss_length=(1, 10), num_outs=100):
        """
        Generates Markov text of length between range.
        """
        if not self.dict:
            self.init_dictionary()
        while len(self.generated['captions']) < num_outs:
            start = random.choice(list(self.dict.keys()))
            sentence = [start]
            sentence_length = random.randint(poss_length[0], poss_length[1])
            while len(sentence) < sentence_length and sentence[-1] in self.dict:
                if sentence[-1] in self.dict:
                    sentence.append(random.choice(self.dict[sentence[-1]]))
            self.generated['captions'].append(' '.join(sentence))
            print(self.generated)

        with open('markov.json', 'w+') as file:
            json.dump(self.generated, file)

if __name__ == '__main__':
    MarkovText('/Users/alice/Projects/subtext/data/youtube-new/USvideos.csv', 'csv', 'description').gen_text((1000, 1000), 10)
