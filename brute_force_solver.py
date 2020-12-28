import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_happiness
import sys
import random

def solve(G, s):
    """
    Args:
        G: networkx.Graph
        s: stress_budget
    Returns:
        D: Dictionary mapping for student to breakout room r e.g. {0:2, 1:0, 2:1, 3:2}
        k: Number of breakout rooms
    """

    nodes = list(G.nodes())

    def partition(collection):
        if len(collection) == 1:
            yield [ collection ]
            return

        first = collection[0]
        for smaller in partition(collection[1:]):
            for n, subset in enumerate(smaller):
                yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
            yield [ [ first ] ] + smaller


    max_happiness = 0
    max_list = None
    for n, p in enumerate(partition(nodes)):
        total_happiness = 0
        is_valid = True
        for group in p:
            edges = list(filter(lambda edge: edge[0] in group and edge[1] in group, G.edges(data=True)))
            stress = sum(edge[2]['stress'] for edge in edges)
            if stress > s / len(p):
                is_valid = False
                break
            happiness = sum(edge[2]['happiness'] for edge in edges)
            total_happiness += happiness
        if is_valid and total_happiness > max_happiness:
            max_happiness = total_happiness
            max_list = p
            
    max_dict = {}
    for i, group in enumerate(max_list):
        for member in group:
            max_dict[member] = i
    assert is_valid_solution(max_dict, G, s, len(max_list))
    re_max_happiness = calculate_happiness(max_dict, G)

    if re_max_happiness != max_happiness:
        print('shiva', re_max_happiness, max_happiness, max_dict)

    return max_dict



# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G, s = read_input_file(path)
#     D, k = solve(G, s)
#     assert is_valid_solution(D, G, s, k)
#     print("Total Happiness: {}".format(calculate_happiness(D, G)))
#     write_output_file(D, 'out/test.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
# if __name__ == '__main__':
#     inputs = glob.glob('file_path/inputs/*')
#     for input_path in inputs:
#         output_path = 'file_path/outputs/' + basename(normpath(input_path))[:-3] + '.out'
#         G, s = read_input_file(input_path, 100)
#         D, k = solve(G, s)
#         assert is_valid_solution(D, G, s, k)
#         cost_t = calculate_happiness(T)
#         write_output_file(D, output_path)
