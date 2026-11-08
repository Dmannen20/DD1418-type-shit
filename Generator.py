import math
import argparse
import codecs
from collections import defaultdict
import random

"""
This file is part of the computer assignments for the course DD1418 at KTH.
"""

class Generator(object) :
    """
    This class generates words from a language model.
    """
    def __init__(self):
    
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
        # Important that it is named self.logProb for the --check flag to work
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


    def read_model(self,filename):
        """
        Reads the contents of the language model file into the appropriate data structures.

        :param filename: The name of the language model file.
        :return: True if the entire file could be processed, False otherwise.
        """

        try:
            with codecs.open(filename, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))
                # YOUR CODE HERE
                for q in range(self.unique_words):
                    # jag tog bort map(float osv) för det blev konstigt senare
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

    def generate(self, w, n):
        """
        Generates and prints n words, starting with the word w, and following the distribution
        of the language model.
        """ 
        # YOUR CODE HERE
        current_word = w
        
        # this list holds all randomly generated words
        words = [current_word]
        for _ in range(n - 1):
            probs = self.bigram_prob[self.index[current_word]] #  {next_word_id: logprob, next_word_id: logprob...}
            if len(probs) == 0: # if empty
                print(f"died at _ = {_}")
                next_id = random.randrange(self.unique_words)
                current_word = self.word[next_id]
                words.append(current_word)
                continue;# SLUMPA FRAM ORD
            
            ids_of_coming_word = list(probs.keys())
            
            # list of probabilites (not logged)
            weights = [math.exp(log_p) for log_p in probs.values()]
            
            # gives "random" next word, according to weights 
            next_id = random.choices(ids_of_coming_word, weights=weights)[0] # [0] because choice returns a list
            current_word = self.word[next_id]
            words.append(current_word)
            
        # glues the words of list "words" together with " "
        print (" ".join(words))
                

        pass


def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='BigramTester')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file with language model')
    parser.add_argument('--start', '-s', type=str, required=True, help='starting word')
    parser.add_argument('--number_of_words', '-n', type=int, default=100)

    arguments = parser.parse_args()

    generator = Generator()
    generator.read_model(arguments.file.strip())
    generator.generate(arguments.start.strip(),arguments.number_of_words)

if __name__ == "__main__":
    main()
