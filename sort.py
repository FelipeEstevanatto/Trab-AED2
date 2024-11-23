# https://www.geeksforgeeks.org/sorting-array-strings-words-using-trie/
import os
import cProfile
import csv

from trie_sort import trie_sort
from radix_sort import radix_sort
# set the current working directory
os.chdir(os.path.dirname(__file__))

# Read the olist_orders_dataset.csv file
csv_file = open('datasets/olist_geolocation_dataset_normalized.csv', 'r')
data = list(csv.reader(csv_file))

# sorted = trie_sort(data, 3)
# sorted = radix_sort(data, 3)

# # # save the sorted data to a new CSV file
# with open('datasets/olist_geolocation_dataset_sorted.csv', 'w', newline='', encoding='utf-8') as csv_file:
#     writer = csv.writer(csv_file)
#     writer.writerows(sorted)

# Profile the main function
# cProfile.run('trie_sort(data, 3)')

cProfile.run('radix_sort(data, 3)')