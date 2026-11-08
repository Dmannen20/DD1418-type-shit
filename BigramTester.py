#  -*- coding: utf-8 -*-
import math
import argparse
import re
import codecs
from collections import defaultdict

"""
This file is part of the computer assignments for the course DD1418 at KTH.
"""

class BigramTester(object):
    def __init__(self):
        """
        This class reads a language model file and a test file, and computes
        the entropy of the latter. 
        """
        # The mapping from words to identifiers.
        self.index = {}

        # The mapping from identifiers to words.
        self.word = {}

        # An array holding the unigram counts.
        self.unigram_count = {}

        # The bigram log-probabilities.
        self.bigram_prob = defaultdict(dict)

        # Number of unique words (word forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0

        # The average log-probability (= the estimation of the entropy) of the test corpus.
        self.logProb = 0

        # The identifier of the previous word processed in the test corpus. Is -1 if the last word was unknown.
        self.last_index = -1

        # The fraction of the probability mass given to unknown words.
        self.lambda3 = 0.000001

        # The fraction of the probability mass given to unigram probabilities.
        self.lambda2 = 0.01 - self.lambda3

        # The fraction of the probability mass given to bigram probabilities.
        self.lambda1 = 0.99

        # The number of words processed in the test corpus.
        self.test_words_processed = 0


    def read_model(self, filename):
        """
        Reads the contents of the language model file into the appropriate data structures.

        :param filename: The name of the language model file.
        :return: <code>true</code> if the entire file could be processed, false otherwise.
        """

        try:
            with codecs.open(filename, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))
                # YOUR CODE HERE
                # Denna kod är kopierad från Generator.py.
                
                for q in range(self.unique_words):
                    row = f.readline().strip().split(' ')
                    idx = int(row[0])
                    self.index[row[1]] = idx # ordet är nyckeln. Vi assignar dess id
                    self.word[idx] = row[1]
                    self.unigram_count[row[1]] = int(row[2]) # ordet (row[1]) är nyckeln. 
                                    
                
                while True:
                    row = f.readline().strip().split(' ')
                                    
                    if row[0] == '-1':
                        break
                                    
                    prev_index = int(row[0])
                    current_index = int(row[1])
                    log_prob = float(row[2])
                    self.bigram_prob[prev_index][current_index] = log_prob
                    
                return True
        except IOError:
            print("Couldn't find bigram probabilities file {}".format(filename))
            return False


    def compute_entropy_cumulatively(self, word):
        # YOUR CODE HERE

        unigram_prob = self.unigram_count.get(word, 0)/ self.total_words # what happens if a weird word appears
        self.test_words_processed += 1 

        # local variable!
        bigram_prob_linear = 0
        
        # This is to make sure bigram_prob_linear remains 0 if no match
        # (if we have a previos word) AND (one of the keys = word)
        if self.last_index != -1 and word in self.index:
            log_p = self.bigram_prob[self.last_index].get(self.index[word])
            if log_p is not None:
                bigram_prob_linear = math.exp(log_p)
        
        # enligt den givna formeln
        wtf = math.log(self.lambda1 * bigram_prob_linear + self.lambda2*unigram_prob + self.lambda3)
        
        # enligt formeln
        N = self.test_words_processed
        
        old_log_average= self.logProb * (N-1)
        # contribution is -wtf/N
        self.logProb = old_log_average + (-wtf)/N

        # return -1 if there are no such word
        self.last_index = self.index.get(word, -1)
        pass

    def process_test_file(self, test_filename):
        """
        Reads and processes the test file one word at a time. 

        :param test_filename: The name of the test corpus file.
        :return: True if the entire file could be processed, False otherwise.
        """
        try:
            with codecs.open(test_filename, 'r', 'utf-8') as f:
                text = f.read().encode('utf-8').decode().lower()
                self.tokens = re.findall(r"[\w'-]+|[\".,!?;]", text)
                for token in self.tokens:
                    self.compute_entropy_cumulatively(token)
            return True
        except IOError:
            print('Error reading testfile')
            return False


def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='BigramTester')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file with language model')
    parser.add_argument('--test_corpus', '-t', type=str, required=True, help='test corpus')

    arguments = parser.parse_args()

    bigram_tester = BigramTester()
    bigram_tester.read_model(arguments.file.strip())
    bigram_tester.process_test_file(arguments.test_corpus.strip())
    print('Read {0:d} words. Estimated entropy: {1:.2f}'.format(bigram_tester.test_words_processed, bigram_tester.logProb))

if __name__ == "__main__":
    main()
