from Helpers import *
from HuffmanCustom import *

alphabet  = ['a','b','c','d','e','f']
probabilities = [0.05, 0.1, 0.15, 0.18, 0.22, 0.3]



n = 1000
sequence = generate_a_sequence(probabilities, alphabet, n)

#huffman encoding block size 1
code_book_1 = generate_a_codebook(probabilities, alphabet)
first_encoding = huffman_encode(sequence,code_book_1)
stats1 = get_statistics(sequence,first_encoding,code_book_1,alphabet,probabilities)

#huffman encoding block size 2
alphabet_len_2 =[]
probabilities_len_2 = []
for i in range(len(probabilities)):
    for j in range(len(probabilities)):
        alphabet_len_2.append(alphabet[i]+alphabet[j])
        probabilities_len_2.append(probabilities[i]*probabilities[j])

sequence_2 = []
for i in  range(0, len(sequence)-1, 2):
    sequence_2.append(sequence[i]+sequence[i+1])

code_book_2 = generate_a_codebook(probabilities_len_2,alphabet_len_2)
second_encoding = huffman_encode(sequence_2,code_book_2)
stats2 = get_statistics(sequence_2,second_encoding,code_book_2,alphabet_len_2,probabilities_len_2)


#huffman encoding block size 2, probabilities flipped
probabilities = [0.3, 0.1, 0.15, 0.18, 0.22, 0.05]

#use new probabilities for generation of sequence, split it into size 2 blocks
sequence_3 = generate_a_sequence(probabilities, alphabet, n)
sequence_4 = []
for i in  range(0, len(sequence_3)-1, 2):
    sequence_4.append(sequence_3[i]+sequence_3[i+1])

#old probabilities for compression
third_encoding = huffman_encode(sequence_4,code_book_2)     

#new probabilities for calculating statistics
probabilities_len_2 = []
for i in range(len(probabilities)):
    for j in range(len(probabilities)):
        probabilities_len_2.append(probabilities[i]*probabilities[j])

stats3 = get_statistics(sequence_4,third_encoding,code_book_2,alphabet_len_2,probabilities_len_2)

print(stats1)

print(stats2)

print(stats3)