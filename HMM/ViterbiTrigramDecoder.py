from Key import Key
import math
import sys
import numpy as np
import codecs
import argparse

"""
This file is part of the computer assignments for the course DD1418 at KTH.
"""

class ViterbiTrigramDecoder(object):
    """
    This class implements Viterbi decoding using trigram probabilities in order
    to correct keystroke errors.
    """
    def init_a(self, filename):
        """
        Reads the trigram probabilities (the 'A' matrix) from a file.
        """
        with codecs.open(filename, 'r', 'utf-8') as f:
            for line in f:
                i, j, k, d = [func(x) for func, x in zip([int, int, int, float], line.strip().split(' '))]
                self.a[i][j][k] = d


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
            self.b[i][i] = np.log((10 - len(cs))/10.0)


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
        self.v = np.zeros((len(s), Key.NUMBER_OF_CHARS, Key.NUMBER_OF_CHARS), dtype='double')
        self.v[:,:,:] = -float("inf")
        self.backptr = np.zeros((len(s), Key.NUMBER_OF_CHARS, Key.NUMBER_OF_CHARS), dtype='int')

        # Initialization

        # backpointer[tid, förraIndex, nuvarande]
        self.backptr[0,Key.START_END,:] = Key.START_END
        # b är fortfarande 2D
        self.v[0,Key.START_END,:] = self.a[Key.START_END,Key.START_END,:] + self.b[:,index[0]]


        # YOUR CODE HERE

        # Induction step
        last_real_char=None

        for t in range(1,len(index)):
            observed_index = index[t]

            for k in range(0,Key.NUMBER_OF_CHARS):
                
                

                for j in range(0,Key.NUMBER_OF_CHARS):
                    max_viterbi = -float("inf") # potential smoothing needed??
                    best_i = 0

                    for i in range(0,Key.NUMBER_OF_CHARS):
                        # let us check the previous "time"/"row" for the highest viterbi value
                        
                        #implementerat enligt def. Var medveten om att ordningen vänds
                        pot_max_viterbi = self.v[t-1, i,j] + self.a[i,j,k] + self.b[k,observed_index]
                        

                        if pot_max_viterbi > max_viterbi:
                            max_viterbi = pot_max_viterbi
                            best_i = i

                    self.v[t,j,k] = max_viterbi
                    self.backptr[t,j,k] = best_i # iffy

        #Nu vill vi hitta sista riktiga bokstaven i strängen
        max_final_viterbi = -float("inf")
        # Loopar genom alla 30 möjliga tecken
        for j in range(Key.NUMBER_OF_CHARS):
            
            # Plockar ut sista för varje iteration
            last_value = self.v[len(index)-1,j,Key.START_END]

            # Vi letar efter största möjliga sista värde
            if last_value > max_final_viterbi:
                max_final_viterbi = last_value
                # Bokstaven med störst viterbi blir vår sista bokstav
                last_real_char = j

        # let us backtrace
        result_list = []
        # I praktiken blir det current state som definierar vilken kolumn vi är i "apparatrymden"/matrisen
        # och t står för var i ordet vi är.
        current_state = Key.START_END
        previous_state = last_real_char
        # for loop exkluderar -1, dvs vi gör en baklängesloop av ordets längd till 0
        for t in range(len(s) - 1, 0, -1):
            
            # startar i matrisen längst ner i högra hörnet.
            pointer_double_previous_index = self.backptr[t,previous_state,current_state]
        
            # Vid slutet, mellanslag och början är current state en start/stop symbol
            if previous_state != Key.START_END:
                current_char = Key.index_to_char(previous_state)
                result_list.append(current_char)
            else:
                result_list.append(" ")
                
            current_state = previous_state
            previous_state = pointer_double_previous_index
            
            

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

        # The trigram stats.
        self.a = np.zeros((Key.NUMBER_OF_CHARS, Key.NUMBER_OF_CHARS, Key.NUMBER_OF_CHARS), dtype='double')

        # The observation matrix.
        self.b = np.zeros((Key.NUMBER_OF_CHARS, Key.NUMBER_OF_CHARS), dtype='double')

        # Pointers to retrieve the topmost hypothesis.
        backptr = None

        if filename: self.init_a(filename)
        self.init_b()



    # ------------------------------------------------------

def main():

    parser = argparse.ArgumentParser(description='ViterbiTrigram decoder')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', type=str, help='decode the contents of a file')
    group.add_argument('--string', '-s', type=str, help='decode a string')
    parser.add_argument('--probs', '-p', type=str,  required=True, help='trigram probabilities file')

    arguments = parser.parse_args()

    if arguments.file:
        with codecs.open(arguments.file, 'r', 'utf-8') as f:
            s1 = f.read().replace('\n', ' ')
    elif arguments.string:
        s1 = arguments.string
    s1 = s1.replace('\r', '')


    # Give the filename of the trigram probabilities as a command line argument
    d = ViterbiTrigramDecoder(arguments.probs)

    # Append two extra "END" symbols to the input string, to indicate end of sentence. 
    result = d.viterbi(s1 + Key.index_to_char(Key.START_END) + Key.index_to_char(Key.START_END))

    print(result)

if __name__ == "__main__":
    main()
