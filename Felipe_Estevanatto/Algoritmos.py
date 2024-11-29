# Made with the help of ChatGPT

# Radix Sort
def radix_sort(data, sort_column):
    # Get the maximum length of the strings in the specified column
    max_length = max(len(row[sort_column]) for row in data)

    # Sort from the least significant character to the most significant character
    for i in range(max_length - 1, -1, -1):
        # Initialize 256 buckets for each ASCII character
        buckets = [[] for _ in range(256)]
        
        # Distribute the rows into buckets based on the current character index
        for row in data:
            if i < len(row[sort_column]):
                char_index = ord(row[sort_column][i])
            else:
                char_index = 0  # Use 0 for padding if the index is out of range
            buckets[char_index].append(row)
        
        # Flatten the buckets back into the data list
        data = []
        for bucket in buckets:
            data.extend(bucket)
    
    return data

# Trie Sort
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.data = []  # To store the count of occurrences

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key, row):
        node = self.root
        for char in key:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.data.append(row)

    def _traverse_dfs(self, node, prefix, result):
        if node.is_end_of_word:
            for row in node.data:
                result.append((prefix, row))
        for char in sorted(node.children.keys()):
            self._traverse_dfs(node.children[char], prefix + char, result)

    def sort(self):
        result = []
        self._traverse_dfs(self.root, "", result)
        return result

def trie_sort(data, sort_column):
    trie = Trie()
    for row in data:
        trie.insert(row[sort_column], row)

    # Retrieve the sorted data
    sorted_data = trie.sort()
    return [row for _, row in sorted_data]

# Benchmark framework
import os
import cProfile
import csv
import io
import pstats
from trie_sort import trie_sort
from radix_sort import radix_sort
from memory_profiler import memory_usage

# Set the current working directory
os.chdir(os.path.dirname(__file__))

def read_csv(file_path):
    with open(file_path, 'r') as csv_file:
        return list(csv.reader(csv_file))

def average(stats, count):
    stats.total_calls /= count
    stats.prim_calls /= count
    stats.total_tt /= count

    for func, source in stats.stats.items():
        cc, nc, tt, ct, callers = source
        stats.stats[func] = (cc/count, nc/count, tt/count, ct/count, callers)

    return stats

def best_of_profillings(target_profile_function, count, *args):
    output_stream = io.StringIO()
    profiller_status = pstats.Stats(stream=output_stream)
    mem_usage = []

    for index in range(count):
        profiller = cProfile.Profile()
        profiller.enable()

        mem_usage.append(memory_usage((target_profile_function, args)))

        profiller.disable()
        profiller_status.add(profiller)

        print('Profiled', '%.3f' % profiller_status.total_tt, 'seconds at', index,
              'for', target_profile_function.__name__, flush=True)

    average(profiller_status, count)
    profiller_status.sort_stats("time")
    profiller_status.print_stats()

    avg_mem_usage = [sum(x)/len(x) for x in zip(*mem_usage)]
    print(f"Average memory usage for {target_profile_function.__name__}: {avg_mem_usage} MiB")

    return "\nProfile results for %s\n%s" % (target_profile_function.__name__, output_stream.getvalue())

if __name__ == "__main__":
    # Read the CSV file
    data = read_csv('olist_geolocation_dataset_normalized.csv')

    # Profile and measure memory usage during sorting
    heavy_lifting_result = best_of_profillings(radix_sort, 10, data, 3)
    print("Radix sort\n" + heavy_lifting_result)

    # Profile and measure memory usage during trie sort
    heavy_lifting_result = best_of_profillings(trie_sort, 10, data, 3)
    print("Trie sort\n" + heavy_lifting_result)

# Github will full code
# https://github.com/FelipeEstevanatto/Trab-AED2