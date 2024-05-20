from typing import TypeVar
import numpy as np
from typeguard import typechecked

T = TypeVar('T')

class EncodingStatistics:
    def __init__(self, entropy_real: float, entropy_codebook: float, expected_length_real: float, expected_length_codebook: float, average_length: float, compression_ratio: float, symbol_length:float):
        self.entropy_real = entropy_real
        self.expected_length_real = expected_length_real
        self.entropy_codebook = entropy_codebook
        self.expected_length_codebook = expected_length_codebook
        self.average_length = average_length
        self.compression_ratio = compression_ratio
        self.symbol_length = symbol_length
    def __str__(self):
        entropy = ""
        if(self.entropy_real == self.entropy_codebook or self.entropy_codebook == 0):
            entropy = f"Entropy: {round(self.entropy_real,4)}"
        else:
            entropy = f"""
    Entropy (Real): {round(self.entropy_real,4)}
    Entropy (Codebook): {round(self.entropy_codebook,4)}"""

        expected = ""
        if(self.expected_length_real == self.expected_length_codebook or self.expected_length_codebook == 0):
            expected = f"Expected length(bits): {round(self.expected_length_real,4)}"
        else:
            expected = f"""
    Expected length of real probability distribution (bits): {round(self.expected_length_real,4)}
    Expected length of codebooks probability distribution: {round(self.expected_length_codebook,4)}"""
       
        return f"""
    {entropy}
    {expected}
    Average length(bits): {self.average_length}
    Log2 of alphabet length: {round(self.symbol_length,4)}
    Compression Ratio: {round(self.compression_ratio,4)}
    Bounds on expected length: {round(self.entropy_real,4)}<={round(self.expected_length_real,4)}<={round(self.entropy_real,4)+1}"""
    


@typechecked
def generate_a_sequence(probabilities:list[float],alphabet:list[T], length:int) -> list[T]:

    assert np.isclose(sum(probabilities), 1), "Probabilities must sum to 1."

    random_array = np.random.choice(alphabet, length, p=probabilities)

    return random_array.tolist()

# @typechecked
# def get_statistics(sequence:list[T],sequence_compressed:list[T],codebook:dict[T,str],alphabet:list[T], probabilities_real:list[float], probabilities_codebook:list[float]) -> dict[str,float]:
    
#     entropy_real = calculate_entropy(probabilities_real)
    
#     entropy_codebook = calculate_entropy(probabilities_codebook)
    
#     expected_length_real = calculate_expected_length(probabilities_real, codebook, alphabet)
    
#     expected_length_codebook = calculate_expected_length(probabilities_codebook, codebook, alphabet)

#     average_length = sum(len(sequence_compressed[i]) for i in range(len(sequence_compressed))) / len(sequence)

#     compression_ratio = calculate_compression_ratio(sequence,sequence_compressed,alphabet)
    
#     return EncodingStatistics(entropy_real,entropy_codebook,expected_length_real, expected_length_codebook, average_length, compression_ratio)


@typechecked
def get_statistics(sequence:list[T],
                   sequence_compressed:str,
                   codebook:dict[T,str],
                   alphabet:list[T],
                   probabilities:list[float],) -> EncodingStatistics:
    
    entropy_real = calculate_entropy(probabilities)
    
    expected_length_real = calculate_expected_length(probabilities, codebook, alphabet)

    average_length = sum(len(sequence_compressed[i]) for i in range(len(sequence_compressed))) / len(sequence)

    compression_ratio = calculate_compression_ratio(sequence,sequence_compressed,alphabet)
    
    symbol_length_bits = np.log2(len(alphabet))
    
    return EncodingStatistics(entropy_real,0,expected_length_real, 0, average_length, compression_ratio,symbol_length_bits)




def calculate_entropy(probabilities:list[float]) -> float:
    
    entropy = -sum(p * np.log2(p) for p in probabilities if p != 0)
    
    return entropy

def calculate_expected_length(probabilities:list[float],codebook:dict[T,str],alphabet:list[T]) -> float:

    expected_length = sum(len(codebook[symbol]) * probabilities[alphabet.index(symbol)] for symbol in alphabet)
    
    return expected_length

def calculate_compression_ratio(sequence:list[T],sequence_compressed:str,alphabet:list[T]) -> float:
    
    a=len(sequence) * np.log2(len(alphabet))
    b = len(sequence_compressed)
    c = a/b
    
    return c
