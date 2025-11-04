from typing import List

ALGO_KEYWORDS = {
    "dfs": "Depth-First Search",
    "bfs": "Breadth-First Search",
    "dijkstra": "Dijkstra's Shortest Path",
    "bellman-ford": "Bellman-Ford",
    "binary_search": "Binary Search",
    "merge_sort": "Merge Sort",
    "quick_sort": "Quick Sort",
    "fft": "Fast Fourier Transform",
}

def detect_algorithms(code: str) -> List[str]:
    found = set()
    lower = code.lower()
    for key, name in ALGO_KEYWORDS.items():
        if key in lower:
            found.add(name)
    return sorted(found)
