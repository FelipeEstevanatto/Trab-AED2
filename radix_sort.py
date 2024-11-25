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