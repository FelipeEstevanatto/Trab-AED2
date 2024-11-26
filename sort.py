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
    data = read_csv('datasets/olist_geolocation_dataset_normalized.csv')

    # Profile and measure memory usage during sorting
    heavy_lifting_result = best_of_profillings(radix_sort, 10, data, 3)
    print("Radix sort\n" + heavy_lifting_result)

    # Profile and measure memory usage during trie sort
    heavy_lifting_result = best_of_profillings(trie_sort, 10, data, 3)
    print("Trie sort\n" + heavy_lifting_result)