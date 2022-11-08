# import modules
import sys
import os
import itertools
import statistics
from nltk import ngrams
import hashlib
from itertools import combinations
import numpy as np

# class: Simhash
class Simhash:
    # call constructor
    def __init__(self, acc_size, window_size, comb_size):

        # set internal variables
        self.acc_size = acc_size
        self.window_size = window_size

        # set combination size, if bigger than window, take window size instead
        if window_size > comb_size:
            self.comb_size = comb_size
        else:
            self.comb_size = window_size
        self.accumulator = [0]*self.acc_size
        self.window = [-1]*window_size
        self.hash_const = []

        np.random.seed(30)  
        hash_const = np.random.choice(range(acc_size), size=acc_size, replace=False)
        for item in hash_const:
            self.hash_const.append(item)

    # class method: hash combinations
    def hashenator(self, s):
        result = 1
        for item in s:
            result = item * result
        return (result + 3) % self.acc_size

    # class method: calc_digest
    def calc_digest(self, str1):

        # set a local counter to iterate
        counter = 0

        # iterate through string with sliding window of x bytes
        for x in range(counter, len(str1)):
            self.window = str1[x:x+self.window_size]
            counter += 1

            # take each combination of size n
            for combination in itertools.combinations(self.window, self.comb_size):

                # call hash function
                val = self.hashenator(combination)

                # get index of value in hash_const array
                ind = self.hash_const.index(val)

                #increment value at accumulator
                self.accumulator[ind] += 1

        # find median value in accumulator
        median_value = statistics.median(self.accumulator)

        # assign 1 or 0 based on median
        for x in range(0,self.acc_size):
            if self.accumulator[x] <= median_value:
                self.accumulator[x] = 0
            else:
                self.accumulator[x] = 1

        # create list to hold final feature vector
        hash_list = []

        # iterate through each byte and convert to decimal
        for x in range(0,self.acc_size,8):
            new_string = ''
            this_byte = self.accumulator[x:x+8]

            for bit in this_byte:
                new_string += str(bit)
            hash_list.append(int(new_string,2))

        # return final feature vector
        return hash_list

# main function
def main(argv):

    # capture simhash parameters and inputfile name from command line
    acc_size = int(argv[1])
    window_size = int(argv[2])
    ngram_size = int(argv[3])
    infile1 = argv[4]

    # create new Simhash object (Simhash(<accumulator_size><window_size><ngram_size>))
    sim = Simhash(acc_size, window_size, ngram_size)

    # open input file and read to str1 as bytes object
    with open(infile1, 'rb') as file1:

        # read in file...
        str1 = file1.read()

        # break into list of bytes objects
        strlist = [x for x in str1]

        # call sim.calc_digest
        print(sim.calc_digest(strlist))

if __name__ == '__main__':
    main(sys.argv)
