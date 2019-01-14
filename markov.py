"""
generate.py
Generates captions using Markov chains.
Corpus created using scrape.py.
"""

import random
import json

class MarkovText():
    """
    Generates text using Markov chains.
    """

    def __init__(self, file):
        self.corpus = None
        self.dict = {}
        self.generated = {'captions': []}
        self.read_corpus(file)

    def read_corpus(self, file):
        """
        Reads in text file to serve as corpus.
        Splits text into individual words.
        """
        with open(file, 'r') as filehandle:
            text = json.load(filehandle)
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
            start = random.choice(self.dict.keys())
            sentence = [start]
            sentence_length = random.randint(poss_length[0], poss_length[1])
            while len(sentence) < sentence_length and sentence[-1] in self.dict:
                if sentence[-1] in self.dict:
                    sentence.append(random.choice(self.dict[sentence[-1]]))
            self.generated['captions'].append(' '.join(sentence))

        with open('markov.json', 'w+') as file:
            json.dump(self.generated, file)

if __name__ == '__main__':
    MarkovText('scraped/captions.json').gen_text((1, 20), 1000)
