from Key import Key
import math
import sys
import numpy as np
import codecs
import argparse

"""
This file is part of the computer assignments for the course DD1418 at KTH.
"""

class ViterbiBigramDecoder(object):
    """
    This class implements Viterbi decoding using bigram probabilities in order
    to correct keystroke errors.
    """
    def init_a(self, filename):
        """
        Reads the bigram probabilities (the 'A' matrix) from a file.
        """
        with codecs.open(filename, 'r', 'utf-8') as f:
            for line in f:
                i, j, d = [func(x) for func, x in zip([int, int, float], line.strip().split(' '))]
                self.a[i][j] = d


    # ------------------------------------------------------


    def init_b(self):
        """
        Initializes the observation probabilities (the 'B' matrix).
        """
        for i in range(Key.NUMBER_OF_CHARS):
            cs = Key.neighbour[i]

            # Initialize all log-probabilities to some small value.
            for j in range(Key.NUMBER_OF_CHARS):
                self.b[i][j] = -float("inf")

            # All neighbouring keys are assigned the probability 0.1
            for j in range(len(cs)):
                self.b[i][Key.char_to_index(cs[j])] = math.log( 0.1 )

            # The remainder of the probability mass is given to the correct key.
            self.b[i][i] = math.log((10 - len(cs))/10.0)


    # ------------------------------------------------------



    def viterbi(self, s):
        """
        Performs the Viterbi decoding and returns the most likely
        string.
        """
        # First turn chars to integers, so that 'a' is represented by 0,
        # 'b' by 1, and so on.
        index = [Key.char_to_index(x) for x in s]

        # The Viterbi matrices
        self.v = np.zeros((len(s), Key.NUMBER_OF_CHARS))
        self.v[:,:] = -float("inf")
        self.backptr = np.zeros((len(s), Key.NUMBER_OF_CHARS), dtype='int')

        # Initialization
        self.backptr[0,:] = Key.START_END
        self.v[0,:] = self.a[Key.START_END,:] + self.b[:,index[0]]


        # Induction step

        # YOUR CODE HERE


        for j in range(1,len(index)):
            observed_index = index[j]

            for k in range(0,Key.NUMBER_OF_CHARS):
                
            
                max_viterbi = -float("inf") # potential smoothing needed??

                for i in range(0,Key.NUMBER_OF_CHARS):
                    # let us check the previous "time"/"row" for the highest viterbi value
                    
                    #implementerat enligt def. Var medveten om att ordningen vänds
                    pot_max_viterbi = self.v[j-1, i] + self.a[i,k] + self.b[k,observed_index]

                    if pot_max_viterbi > max_viterbi:
                        max_viterbi = pot_max_viterbi
                        self.backptr[j,k] = i # j,k är nuvarande koordinat, som pekar på föregående i som maximerar viterbi


                self.v[j, k] = max_viterbi


        # Finally return the result
        result_list = []
        # I praktiken blir det current state som definierar vilken kolumn vi är i "apparatrymden"/matrisen
        # och t står för var i ordet vi är.
        current_state = Key.START_END
        # for loop exkluderar -1, dvs vi gör en baklängesloop av ordets längd till 0
        for t in range(len(s) - 1, -1, -1):
            
            # startar i matrisen längst ner i högra hörnet.
            pointer_previous_index = self.backptr[t,current_state]
        
            # Vid slutet, mellanslag och början är current state en start/stop symbol
            if pointer_previous_index != Key.START_END:
                current_char = Key.index_to_char(pointer_previous_index)
                result_list.append(current_char)
            else:
                result_list.append(" ")

            current_state = pointer_previous_index

        # gör listan till en sträng
        result_string = "".join(result_list)
        # Vänder på strängen
        result_string = result_string[::-1]

        # REPLACE THE LINE BELOW WITH YOUR CODE

        return result_string


    # ------------------------------------------------------



    def __init__(self, filename=None):
        """
        Constructor: Initializes the A and B matrices.
        """
        # The trellis used for Viterbi decoding. The first index is the time step.
        self.v = None

        # The bigram stats.
        self.a = np.zeros((Key.NUMBER_OF_CHARS, Key.NUMBER_OF_CHARS))

        # The observation matrix.
        self.b = np.zeros((Key.NUMBER_OF_CHARS, Key.NUMBER_OF_CHARS))

        # Pointers to retrieve the topmost hypothesis.
        backptr = None

        if filename: self.init_a(filename)
        self.init_b()



    # ------------------------------------------------------


def main():

    parser = argparse.ArgumentParser(description='ViterbiBigramDecoder')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', type=str, help='decode the contents of a file')
    group.add_argument('--string', '-s', type=str, help='decode a string')
    parser.add_argument('--probs', '-p', type=str,  required=True, help='bigram probabilities file')

    arguments = parser.parse_args()

    if arguments.file:
        with codecs.open(arguments.file, 'r', 'utf-8') as f:
            s1 = f.read().replace('\n', ' ')
    elif arguments.string:
        s1 = arguments.string
    s1 = s1.replace('\r', '')
    
    # Give the filename of the bigram probabilities as a command line argument
    d = ViterbiBigramDecoder(arguments.probs)

    # Append an extra "END" symbol to the input string, to indicate end of sentence. 
    result = d.viterbi(s1 + Key.index_to_char(Key.START_END))

    print(result)


if __name__ == "__main__":
    main()
