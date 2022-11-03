# import modules
import sys
import os
import itertools
import statistics
from nltk import ngrams
from itertools import permutations
from itertools import combinations

# class: Simhash
class Simhash():
	def __init__(self):
		self.accumulator = [0]*256
		window = [-1]*5
		# self.counter = 0

	def calc_digest(self, str1):
		counter = 0

		# iterate through string with sliding window of 5 bytes
		for x in range(counter, len(str1)):
			window = str1[x:x+5]
			counter += 1

			# calculate trigrams
			n = 3
			trigrams = ngrams(window, n)

			for ngram in trigrams:
				for item in ngram:
					current_int = int.from_bytes(item, byteorder=sys.byteorder)
					hash_index = self.onebyte_hash(current_int)
					self.accumulator[hash_index] += 1
		# print(self.accumulator)
		median_value = statistics.median(self.accumulator)
		for x in range(0,256):
			if self.accumulator[x] <= median_value:
				self.accumulator[x] = 0
			else:
				self.accumulator[x] = 1

		# print(self.accumulator)

		for x in range(0,256,8):
			new_string = ''
			this_byte = self.accumulator[x:x+8]
			for bit in this_byte:
				new_string += str(bit)
			print(new_string)

		# byte_list = []

		# for x in range(0,256,8):
		# 	current_hex = self.accumulator[x:x+8]
		# 	hex_string = ''.join([str(x) for x in current_hex])
		# 	val = hex(int(hex_string))
		# 	print(val)


	def onebyte_hash(self, s):
		return hash(s) % 256

# main function
def main(argv):

	# capture file name from command line
	infile1 = argv[1]

	# create new Simhash object
	sim = Simhash()

	# open input file and read to str1 as bytes object
	with open(infile1, 'rb') as file1:

		# read in file...
		str1 = file1.read()

		# break into list of bytes objects
		str1 = str1.split()

		# call sim.calc_digest
		sim.calc_digest(str1)


if __name__ == '__main__':
	main(sys.argv)
