import regex as re

def initialize_vocab(special_tokens: list[str]):

    vocab_dict = {}

    for index, value in enumerate(special_tokens):
        vocab_dict[index] = value.encode("utf-8")

    for i in range(256):
        vocab_dict[i + len(special_tokens)] = bytes([i])

    return vocab_dict

def frequency_dict(s: str):
    PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    
    count = {}

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

toy_text = "low low low low low lower lower widest widest widest newest newest newest newest newest newest"
x = frequency_dict(toy_text)
print(x)
y = count_paris(x)
print(y)
max_pair = get_merging_pair(y)
print(max_pair)
new_dict = complete_merge(max_pair, x)
print(new_dict)

# counts = frequency_dict(toy_text)
# for iteration in range(6):
#     pairs = count_paris(counts) # Corrected your function typo name here!
#     if not pairs:
#         break
#     best_pair = get_merging_pair(pairs)
#     counts = complete_merge(best_pair, counts)
#     print(f"Merge {iteration + 1}: Unified {best_pair}")

# print(counts)