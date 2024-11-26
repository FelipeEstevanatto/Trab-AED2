import os
import csv
import matplotlib.pyplot as plt

# Set the current working directory
os.chdir(os.path.dirname(__file__))

def read_csv(file_path):
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skip the header
        return list(reader)

def plot_top_cities(data, top_n=10):
    cities = {}
    for row in data:
        city = row[3]
        if city in cities:
            cities[city] += 1
        else:
            cities[city] = 1

    # Sort cities by occurrences and take the top N
    sorted_cities = dict(sorted(cities.items(), key=lambda x: x[1], reverse=True))
    top_cities = dict(list(sorted_cities.items())[:top_n])
    
    # Aggregate the rest into "Others"
    others_count = sum([count for city, count in sorted_cities.items() if city not in top_cities])
    top_cities["Others"] = others_count

    plt.bar(top_cities.keys(), top_cities.values())
    plt.xticks(rotation=90)
    plt.title(f"Top {top_n} Cidades por Ocorrências")
    plt.xlabel("City")
    plt.ylabel("Ocorrências")

    plt.show()

def plot_most_cited_city_by_state(data):
    state_city_counts = {}
    for row in data:
        state = row[4]
        city = row[3]
        if state not in state_city_counts:
            state_city_counts[state] = {}
        if city in state_city_counts[state]:
            state_city_counts[state][city] += 1
        else:
            state_city_counts[state][city] = 1

    most_cited_city_by_state = {}
    for state, cities in state_city_counts.items():
        most_cited_city = max(cities, key=cities.get)
        most_cited_city_by_state[state] = most_cited_city

    counts = [state_city_counts[state][most_cited_city_by_state[state]] for state in most_cited_city_by_state]

    plt.bar(most_cited_city_by_state.keys(), counts)
    plt.xticks(rotation=90)
    plt.title("Quantidade de citações por Estado")
    plt.xlabel("Estado")
    plt.ylabel("Quantidade")

    # Add the absolute value on top of each bar
    for i, count in enumerate(counts):
        plt.text(i, count, str(count), ha='center', va='bottom')

    plt.show()

if __name__ == "__main__":
    # Read the CSV file
    data = read_csv('output/sorted_geolocation_dataset.csv')
    
    # Plot the top cities
    plot_top_cities(data, top_n=10)  # Adjust top_n as needed
    
    # Plot the most cited city by state
    plot_most_cited_city_by_state(data)

# Run the script and view the graphs
# python graph.py