# import solver as sv
import brute_force_solver as bs
import parse as pv
import os
from utils import is_valid_solution, calculate_happiness

for filename in os.listdir('outputs/small'):
    os.rename('outputs/small/' + filename, 'outputs/small/' + filename.split(".")[0] + '.out')
    # G, S = pv.read_input_file('inputs/small/' + filename)
    # output_dict = bs.solve(G, S)
    # pv.write_output_file(output_dict, 'outputs/small/' + filename)