import os
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('k', type=int, help='The top k parameters are returned')
parser.add_argument('input', default='xplore/',
                    help='The folder containing the data')
args = parser.parse_args()


if __name__ == '__main__':
    cpi = {}

    if args.input[-1] != '/':
        args.input += '/'

    for benchmark in os.listdir(args.input):
        for params in os.listdir(args.input + benchmark):
            # Current expirement
            with open(args.input + '{}/{}/stats.txt'.format(benchmark, params)) as f:
                # Get CPI from stats.txt
                for i, line in enumerate(f):
                    if i == 28:
                        if params in cpi:
                            cpi[params] += float(line.split()[1])
                        else:
                            cpi[params] = float(line.split()[1])
                        break
    
    top = sorted(cpi.items(), key = lambda kv:(kv[1], kv[0]))
    n_bench = len(os.listdir(args.input))
    
    print('\033[1m', end='') # BOLD
    print('  #| i-cache size|i-cache assoc|d-cache size|d-cache assoc|l2-cache size|l2-cache assoc|cache line size| avg. cpi')
    print('\033[0m', end='') # UNBOLD
    for i, (params, cpi) in enumerate(top[:args.k]):
        config = [int(p) for p in params.split('_')]
        
        print('\033[1m', end='') # BOLD
        print('{:3}'.format(i+1), end='|')
        print('\033[0m', end='') # UNBOLD
        
        print('{}'.format(config[0]).center(13), end='|')
        print('{}'.format(config[1]).center(13), end='|')
        print('{}'.format(config[2]).center(12), end='|')
        print('{}'.format(config[3]).center(13), end='|')
        print('{}'.format(config[4]).center(13), end='|')
        print('{}'.format(config[5]).center(14), end='|')
        print('{}'.format(config[6]).center(15), end='|')
        print('{:.2f}'.format(cpi/5).center(8))
