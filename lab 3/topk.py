import os
import argparse
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('k', type=int, help='The top k parameters are returned')
parser.add_argument('--input', default='xplore/',
                    help='The folder containing the data')
args = parser.parse_args()


if __name__ == '__main__':
    edap = {}

    if args.input[-1] != '/':
        args.input += '/'

    for benchmark in os.listdir(args.input):
        for params in os.listdir(args.input + benchmark):
            # Current expirement
            with open(args.input + '{}/{}'.format(benchmark, params)) as f:
                # Get EDAP from file
                energy, delay, area = [float(x) for x in f.read().split()]
                edap[params] += energy * delay * area
    
    top = sorted(edap.items(), key = lambda kv:(kv[1], kv[0]))
    n_bench = len(os.listdir(args.input))
    
    print('\033[1m', end='') # BOLD
    print('  #| i-cache size|i-cache assoc|d-cache size|d-cache assoc|l2-cache size|l2-cache assoc|cache line size| avg. edap')
    print('\033[0m', end='') # UNBOLD
    for i, (params, edap) in enumerate(top[:args.k]):
        config = [int(p) for p in params[:-4].split('_')]
        
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
        print('{:.2f}'.format(edap/5).center(8))
