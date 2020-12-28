# import solver as sv
import greedy_solver as gv
import parse as pv
from utils import is_valid_solution, calculate_happiness

G, S = pv.read_input_file('inputs/large/large-144.in')
D = pv.read_output_file('samples/50.out', G, S)


D = gv.solve(G, S)
# pv.write_output_file(swag[0], '20.out')
# print(calculate_happiness(D, G))
print(is_valid_solution(D, G, S, 1))