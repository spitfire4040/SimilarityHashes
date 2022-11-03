# import modules
import sys
import os
import itertools
import statistics
from nltk import ngrams
from itertools import permutations
from itertools import combinations

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

			# calculate ngrams
			# set size of ngrams
			n = self.ngram_size

			# break current window into xgrams
			xgrams = ngrams(self.window, n)

			# iterate through each xgram for current window
			for ngram in xgrams:

				# iterate through each tuple
				for item in ngram:

					# calculate hash for item and increment accumulator
					current_int = int.from_bytes(item, byteorder=sys.byteorder)
					hash_index = self.onebyte_hash(current_int,self.acc_size)
					self.accumulator[hash_index] += 1

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


	def onebyte_hash(self, s, acc):
		return hash(s) % acc

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
		str1 = str1.split()

		# call sim.calc_digest
		print(sim.calc_digest(str1))


if __name__ == '__main__':
	main(sys.argv)
