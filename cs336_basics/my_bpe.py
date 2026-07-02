import regex as re

def initialize_vocab(special_tokens: list[str]):

    vocab_dict = {}

    for index, value in enumerate(special_tokens):
        vocab_dict[index] = value.encode("utf-8")

    for i in range(256):
        vocab_dict[i + len(special_tokens)] = bytes([i])

    return vocab_dict

def update_vocab(old_vocab: dict, merging_pair: tuple):
    new_token = b''.join(merging_pair)
    new_token_index = len(old_vocab.keys())
    old_vocab[new_token_index] = new_token
    return old_vocab

def frequency_dict(s: str, count: dict):
    PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    
    for match in re.finditer(PAT, s):
        word = match.group().encode("utf-8")
        word_as_bytes = [bytes([x]) for x in word]
        count[tuple(word_as_bytes)] = count.get(tuple(word_as_bytes), 0) + 1

    return count

def count_paris(count: dict):
    pair_count = {}
    for key,value in count.items():
        if len(key) <= 1:
            continue

        for i in range(len(key)-1):
            pair_count[(key[i], key[i+1])] = pair_count.get((key[i], key[i+1]), 0) + value

    return pair_count

def get_merging_pair(pair_count: dict):
    if len(pair_count.values()) < 1:
        return 
    max_val = max(pair_count.values())
    max_keys = [k for k, v in pair_count.items() if v == max_val]
    return max(max_keys)

def complete_merge(merging_pair: tuple, frequency: dict):
    pair_as_list = list(merging_pair)

    new_dict = {}
    for key in frequency.keys():
        temp = list(key)
        i = 0
        while i < (len(temp)-1):
            if temp[i] == pair_as_list[0] and temp[i+1] == pair_as_list[1]:
                temp[i] = temp[i] + temp[i+1]
                temp.pop(i+1)
            else:
                i += 1

        new_dict[tuple(temp)] = frequency.get(key) 

    return new_dict

# Input
# input_path: str  Path to a text file with BPE tokenizer training data.
# vocab_size: int  A positive integer that defines the maximum final vocabulary size (including
# the initial byte vocabulary, vocabulary items produced from merging, and any special tokens).
# special_tokens: list[str]  A list of strings to add to the vocabulary. During training, treat
# them as hard boundaries that prevent merges across their spans, but do not include them when
# computing merge statistics.
# Your BPE training function should return the resulting vocabulary and merges:
# Output
# vocab: dict[int, bytes]  The tokenizer vocabulary, a mapping from int (token ID in the
# vocabulary) to bytes (token bytes).
# merges: list[tuple[bytes, bytes]]  A list of BPE merges produced from training. Each list
# item is a tuple of bytes (<token1>, <token2>), representing that <token1> was merged with
# <token2>. The merges should be ordered by order of creation.

def run_bpe(input_path: str, vocab_size: int, special_token_list: list[str]):
    
    with open(input_path, "r", encoding="utf-8") as file:
        content = file.read()

    special_token_delimeter = "|".join(re.escape(t) for t in special_token_list)
    clean_text =  re.split(special_token_delimeter, content)
    
    merge_list = []
    vocab_dict = initialize_vocab(special_token_list)

    counts = {}
    for chunk in clean_text:
        counts = frequency_dict(chunk, counts)

    i = len(vocab_dict.keys())

    while i < vocab_size:
        pairs = count_paris(counts) # Corrected your function typo name here!
        if not pairs:
            break
        best_pair = get_merging_pair(pairs)
        merge_list.append(best_pair)
        vocab_dict = update_vocab(vocab_dict, best_pair)
        counts = complete_merge(best_pair, counts)

        i+=1
        
    return vocab_dict, merge_list


