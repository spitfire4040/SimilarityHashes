# import modules
import sys
import os
import itertools
import statistics
from nltk import ngrams
import hashlib
from itertools import combinations

TRAN = [ord(x) for x in 
    "\x02\xD6\x9E\x6F\xF9\x1D\x04\xAB\xD0\x22\x16\x1F\xD8\x73\xA1\xAC"\
    "\x3B\x70\x62\x96\x1E\x6E\x8F\x39\x9D\x05\x14\x4A\xA6\xBE\xAE\x0E"\
    "\xCF\xB9\x9C\x9A\xC7\x68\x13\xE1\x2D\xA4\xEB\x51\x8D\x64\x6B\x50"\
    "\x23\x80\x03\x41\xEC\xBB\x71\xCC\x7A\x86\x7F\x98\xF2\x36\x5E\xEE"\
    "\x8E\xCE\x4F\xB8\x32\xB6\x5F\x59\xDC\x1B\x31\x4C\x7B\xF0\x63\x01"\
    "\x6C\xBA\x07\xE8\x12\x77\x49\x3C\xDA\x46\xFE\x2F\x79\x1C\x9B\x30"\
    "\xE3\x00\x06\x7E\x2E\x0F\x38\x33\x21\xAD\xA5\x54\xCA\xA7\x29\xFC"\
    "\x5A\x47\x69\x7D\xC5\x95\xB5\xF4\x0B\x90\xA3\x81\x6D\x25\x55\x35"\
    "\xF5\x75\x74\x0A\x26\xBF\x19\x5C\x1A\xC6\xFF\x99\x5D\x84\xAA\x66"\
    "\x3E\xAF\x78\xB3\x20\x43\xC1\xED\x24\xEA\xE6\x3F\x18\xF3\xA0\x42"\
    "\x57\x08\x53\x60\xC3\xC0\x83\x40\x82\xD7\x09\xBD\x44\x2A\x67\xA8"\
    "\x93\xE0\xC2\x56\x9F\xD9\xDD\x85\x15\xB4\x8A\x27\x28\x92\x76\xDE"\
    "\xEF\xF8\xB2\xB7\xC9\x3D\x45\x94\x4B\x11\x0D\x65\xD5\x34\x8B\x91"\
    "\x0C\xFA\x87\xE9\x7C\x5B\xB1\x4D\xE5\xD4\xCB\x10\xA2\x17\x89\xBC"\
    "\xDB\xB0\xE2\x97\x88\x52\xF7\x48\xD3\x61\x2C\x3A\x2B\xD1\x8C\xFB"\
    "\xF1\xCD\xE4\x6A\xE7\xA9\xFD\xC4\x37\xC8\xD2\xF6\xDF\x58\x72\x4E"]

# class: Simhash
class Simhash:
    # call constructor
    def __init__(self, acc_size, window_size, ngram_size):

        # set internal variables
        self.acc_size = acc_size
        self.window_size = window_size
        self.ngram_size = ngram_size
        self.accumulator = [0]*self.acc_size
        self.window = [-1]*window_size

    # class method: calc_digest
    def calc_digest(self, str1):

        # set a local counter to iterate
        counter = 0

        # iterate through string with sliding window of x bytes
        for x in range(counter, len(str1)):
            self.window = str1[x:x+self.window_size]
            counter += 1

            for combination in itertools.combinations(self.window, self.ngram_size):

                # iterate through each n-length combination for current window
                for comb in combination:

                    # convert int combination to bytes
                    new_comb = comb.to_bytes(2, byteorder=sys.byteorder)
                    # current_int = comb.to_bytes(self.ngram_size, byteorder=sys.byteorder)

                    # call multi-hash function and map to accumulator
                    hash_index = self.multi_hash(comb,self.acc_size)
                    print(hash_index)

        #             # index bucket in accumulator by one
        #             self.accumulator[hash_index] += 1

        # # find median value in accumulator
        # median_value = statistics.median(self.accumulator)

        # # assign 1 or 0 based on median
        # for x in range(0,self.acc_size):
        #     if self.accumulator[x] <= median_value:
        #         self.accumulator[x] = 0
        #     else:
        #         self.accumulator[x] = 1

        # # create list to hold final feature vector
        # hash_list = []

        # # iterate through each byte and convert to decimal
        # for x in range(0,self.acc_size,8):
        #     new_string = ''
        #     this_byte = self.accumulator[x:x+8]

        #     for bit in this_byte:
        #         new_string += str(bit)
        #     hash_list.append(int(new_string,2))

        # # return final feature vector
        # return hash_list


    def multi_hash(self, s, acc):
        m = hashlib.new('sha256')
        m.update(s)
        return (m.hexdigest())

        # return (hash(s) % acc)

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
