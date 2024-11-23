import os
import csv
import re
from unidecode import unidecode

# Set the current working directory
os.chdir(os.path.dirname(__file__))

# Function to normalize a string
def normalize_string(s):
    s = s.replace('4º', 'quarto')  # Replace '4º' with 'quarto'
    s = s.replace('4o', 'quarto')  # Replace '4º' with 'quarto'
    s = unidecode(s)  # Remove accents
    s = re.sub(r'[^a-zA-Z0-9\s]', '', s)  # Remove special characters
    s = s.strip()  # Trim extra spaces
    s = re.sub(r'\s+', ' ', s)  # Replace multiple spaces with a single space
    return s

# Read the olist_geolocation_dataset.csv file and normalize 'geolocation_city' column
with open('datasets/olist_geolocation_dataset.csv', 'r', newline='', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    fieldnames = reader.fieldnames
    rows = []
    for row in reader:
        row['geolocation_city'] = normalize_string(row['geolocation_city'])
        rows.append(row)

# Write the normalized data back to a new CSV file
with open('datasets/olist_geolocation_dataset_normalized.csv', 'w', newline='', encoding='utf-8') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(rows)