from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.children = defaultdict(TrieNode)
        self.is_end_of_word = False
        self.data = []  # To store the count of occurrences

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, key, row):
        node = self.root
        for char in key:
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

    # Recuperar os dados ordenados
    sorted_data = trie.sort()
    return [row for _, row in sorted_data]