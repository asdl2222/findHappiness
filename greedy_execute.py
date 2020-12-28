# import solver as sv
import greedy_solver as gs
import parse as pv
import os
from utils import is_valid_solution, calculate_happiness

count = 0
for filename in os.listdir('inputs/small'):
    print(filename)
    if os.path.isfile('outputs/small/' + filename.split('.')[0] + '.out'):
        continue
    G, S = pv.read_input_file('inputs/small/' + filename)
    output_dict = gs.solve(G, S)
    pv.write_output_file(output_dict, 'outputs/small/' + filename.split('.')[0] + '.out')
