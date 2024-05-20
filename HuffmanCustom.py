import heapq
from typing import List, TypeVar
import numpy as np
from typeguard import typechecked

T = TypeVar('T')

class HuffmanNode:
    def __init__(self, probability: float, symbol: T = None, left: 'HuffmanNode' = None, right: 'HuffmanNode' = None):
        self.probability = probability
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.probability < other.probability

def __create_huffman_tree(probabilities: List[float], alphabet: List[T]) -> HuffmanNode:
    assert np.isclose(sum(probabilities), 1), "Probabilities must sum to 1."
    assert len(alphabet)== len(probabilities), "Alphabet and probabilities must have the same length."

    # Create initial heap of nodes
    heap = [HuffmanNode(prob, sym) for prob, sym in zip(probabilities, alphabet)]
    heapq.heapify(heap)

    # Iterate until the heap contains only one node
    while len(heap) > 1:
        # Remove two nodes with the smallest probabilities
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        # Create a new internal node with these two nodes as children
        merged = HuffmanNode(left.probability + right.probability, left=left, right=right)

        # Add the new node back to the heap
        heapq.heappush(heap, merged)

    # The remaining node is the root of the Huffman tree
    return heap[0]

        
def __build_huffman_dict(node: HuffmanNode, prefix: str = '', huffman_dict: dict[T, str] = None) -> dict[T, str]:
    if huffman_dict is None:
        huffman_dict = {}
    if node.symbol is not None:
        huffman_dict[node.symbol] = prefix
    else:
        __build_huffman_dict(node.left, prefix + '0', huffman_dict)
        __build_huffman_dict(node.right, prefix + '1', huffman_dict)
    return huffman_dict

@typechecked
def generate_a_codebook(probabilities:list[float], alphabet:list[T]) -> dict[T,str]:
    
    huffman_tree = __create_huffman_tree(probabilities, alphabet)
    huffman_dict = __build_huffman_dict(huffman_tree)
    return huffman_dict




def __decode(sequence:str,dictionary:dict[T,str]) -> list[T]:

    reverse_dict = {v: k for k, v in dictionary.items()}
    
    decoded_sequence = []
    current_code = ""
    
    for bit in sequence:
        current_code += bit
        if current_code in reverse_dict:
            decoded_sequence.append(reverse_dict[current_code])
            current_code = ""

    return decoded_sequence


def __encode(sequence:list[T],dictionary:dict[T,str]) -> str:
    assert all(element in dictionary for element in sequence), 'Sequence contains values that are not in the dictionary'
    encoded_seqence = map(dictionary.get, sequence)
    return "".join(encoded_seqence)

@typechecked
def huffman_encode(sequence:list[T],dictionary:dict[T,str]) -> str:
    sequence_encoded = __encode(sequence=sequence,dictionary=dictionary)
    assert sequence == __decode(sequence=sequence_encoded,dictionary=dictionary), 'Something wrong with the code'
    return sequence_encoded

@typechecked
def huffman_decode(sequence:str,dictionary:dict[T,str]) -> list[T]:
    sequence_decoded = __decode(sequence=sequence,dictionary=dictionary)
    assert sequence == __encode(sequence=sequence_decoded,dictionary=dictionary), 'Something wrong with the code'
    return sequence_decoded