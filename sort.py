# https://www.geeksforgeeks.org/sorting-array-strings-words-using-trie/
import os
import cProfile
import csv
import io
import pstats
import cProfile
from trie_sort import trie_sort
from radix_sort import radix_sort
# set the current working directory
os.chdir(os.path.dirname(__file__))

# Read the olist_orders_dataset.csv file
csv_file = open('datasets/olist_geolocation_dataset_normalized.csv', 'r')
data = list(csv.reader(csv_file))

# https://stackoverflow.com/questions/54375392/how-to-calculate-the-average-result-of-several-cprofile-results
def average(stats, count):
    stats.total_calls /= count
    stats.prim_calls /= count
    stats.total_tt /= count

    for func, source in stats.stats.items():
        cc, nc, tt, ct, callers = source
        stats.stats[func] = ( cc/count, nc/count, tt/count, ct/count, callers )

    return stats

def best_of_profillings(target_profile_function, count, *args):
    output_stream = io.StringIO()
    profiller_status = pstats.Stats( stream=output_stream )

    for index in range(count):
        profiller = cProfile.Profile()
        profiller.enable()

        target_profile_function(*args)

        profiller.disable()
        profiller_status.add( profiller )

        print( 'Profiled', '%.3f' % profiller_status.total_tt, 'seconds at', index,
                'for', target_profile_function.__name__, flush=True )

    average( profiller_status, count )
    profiller_status.sort_stats( "time" )
    profiller_status.print_stats()

    return "\nProfile results for %s\n%s" % ( 
           target_profile_function.__name__, output_stream.getvalue() )

# heavy_lifting_result = best_of_profillings(radix_sort, 10, data, 3)
# print(heavy_lifting_result)

sorted = radix_sort(data, 3)

# # save the sorted data to a new CSV file
with open('datasets/olist_geolocation_dataset_sorted.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(sorted)

# Profile the main function
# cProfile.run('trie_sort(data, 3)')

# cProfile.run('radix_sort(data, 3)')
# cProfile.run('merge_sort(data, 3)')

# Run python default sort
# cProfile.run('sorted(data, key=lambda x: x[3])')