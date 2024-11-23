def radix_sort(data, sort_column):
    # Get the maximum length of the strings
    max_length = max(len(row[sort_column]) for row in data)

    for i in range(max_length - 1, -1, -1):
        buckets = [[] for _ in range(256)]
        for row in data:
            char_index = ord(row[sort_column][i]) if i < len(row[sort_column]) else 0
            buckets[char_index].append(row)
        data = [row for bucket in buckets for row in bucket]
    
    return data