#  -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import argparse
import re
import os
from collections import defaultdict
import codecs

# source my_venv/bin/activate

"""
This file is part of the computer assignments for the course DD1418 at KTH. 
"""


class BigramTrainer(object):
    """
    This class constructs a bigram language model from a corpus.
    """

    def process_files(self, filename):
        with codecs.open(filename, 'r', 'utf-8') as f:
            text = f.read().encode('utf-8').decode().lower()
        self.tokens = re.findall(r"[\w'-]+|[\".,!?;]", text)
        print( len(self.tokens) )
        for token in self.tokens: # Detta var kommenterat tidigare
            self.process_token(token) # Och denna också


    def process_token(self, token):
        """
        Processes one word in the training corpus, and adjusts the unigram and
        bigram counts.

        :param token: The current word to be processed.
        """
        # YOUR CODE HERE
        
        self.unigram_count[token] += 1
        self.total_words += 1


        if token not in self.index:

            self.unique_words += 1
            id = len(self.index)
            self.index[token] = id
            self.word[id] = token
        

        if self.last_index != -1:
            self.bigram_count[self.last_index][self.index[token]] += 1
        
        self.last_index = self.index[token]

    def stats(self):
        """s
        Creates a list of rows to print of the language model.
        """
        rows_to_print = []

        # YOUR CODE HERE
        rows_to_print.append(str(self.unique_words) + " " + str(self.total_words))

        for q in self.word: # q är nyckeln i dicken
        
            index = q
            w_q = self.word[q] # ordet
            w_f = self.unigram_count[w_q] # Frekvens av ordet
            rows_to_print.append(str(index) + " " + w_q + " " + str(w_f))
            # print(str(index) + " " + w_q + " " + str(w_f)) test

        for q in self.bigram_count: # q är första ordet i bigramet
            for p in self.bigram_count[q]: # p är andra i bigramet
                numerator = self.bigram_count[q][p]
                denominator = self.unigram_count[self.word[q]]
                if numerator != 0:
                    prob = numerator/denominator
                    p_log = math.log(prob)
                    rows_to_print.append(f"{q} {p} {p_log:.15f}")
        rows_to_print.append("-1")
        return rows_to_print

    def __init__(self):
        """
        Constructor. Processes the file f and builds a language model
        from it.

        :param f: The training file.
        """
    
        # The mapping from words to identifiers.
        self.index = {}

        # The mapping from identifiers to words.
        self.word = {}

        # An array holding the unigram counts.
        self.unigram_count = defaultdict(int)

        """
        The bigram counts. Since most of these are zero (why?), we store these
        in a hashmap rather than an array to save space (and since it is impossible
        to create such a big array anyway).
        """
        self.bigram_count = defaultdict(lambda: defaultdict(int))

        # The identifier of the previous word processed.
        self.last_index = -1

        # Number of unique words (word forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0


def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='BigramTrainer')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file from which to build the language model')
    parser.add_argument('--destination', '-d', type=str, help='file in which to store the language model')

    arguments = parser.parse_args()

    bigram_trainer = BigramTrainer()

    bigram_trainer.process_files(arguments.file.strip())

    stats = bigram_trainer.stats()
    if arguments.destination:
        with codecs.open(arguments.destination.strip(), 'w', 'utf-8' ) as f:
            for row in stats:
                f.write(row + '\n')
    else:
        for row in stats:
            print(row)


if __name__ == "__main__":
    main()
