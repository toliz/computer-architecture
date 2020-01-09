import re
import os
import time
import subprocess
import argparse

FNULL = open(os.devnull, 'w')
LAB2  = '/home/toliz/Desktop/lab 2/'
MCPAT = '/home/toliz/mcpat/'

parser = argparse.ArgumentParser()
parser.add_argument('benchmark', nargs='+', help='Which of the benchmarks to run for')
parser.add_argument('--override', default=False, help='Override current files?')
args = parser.parse_args()

counter = 1
for exp in ['1', '2']:
    for benchmar in args.benchmark:
        for dir in os.listdir(LAB2 + 'xplore-{}/{}'.format(exp, benchmar)):
            start = time.time()
            
            # Don't waste time for already produced results
            if not args.override:
                if os.path.exists('xplore-{}/{}/{}.txt'.format(exp, benchmar, dir)):
                    continue

            stats  = LAB2 + 'xplore-{}/{}/{}/stats.txt'.format(exp, benchmar, dir)
            config = LAB2 + 'xplore-{}/{}/{}/config.json'.format(exp, benchmar, dir)

            # Convert stats and config to xml
            command = MCPAT + 'Scripts/GEM5ToMcPAT.py "{}" "{}" '.format(stats, config) + \
                      MCPAT + 'mcpat/ProcessorDescriptionFiles/inorder_arm.xml -o out.xml'
            subprocess.call('python2 ' + command, stdout=FNULL, stderr=FNULL, shell=True)

            # Run McPAT & read output
            command = MCPAT + 'mcpat/mcpat -infile out.xml -print_level 1 > mcpat.out'
            subprocess.call(command, stdout=FNULL, stderr=FNULL, shell=True)

            with open('mcpat.out') as f:
                mcpatout = f.read()

            # Calculate Area
            mcpatout = mcpatout.splitlines()
            for line in mcpatout:
                if len(line.split()) > 0 and line.split()[0] == 'Area':
                    area = float(line.split()[2])
                    break

            # Calculate delay
            with open(stats) as f:
                delay = float(f.readlines()[11].split()[1])

            # Calculate Energy
            command = MCPAT + 'Scripts/print_energy.py -q mcpat.out "{}"'.format(stats)
            energyout = subprocess.run('python2 ' + command, capture_output=True, shell=True)
            energy = float(energyout.stdout.decode('utf-8').splitlines()[-1].split()[2])

            with open('xplore-{}/{}/{}.txt'.format(exp, benchmar, dir), 'w') as f:
                f.write('{} {} {}'.format(energy, delay, area))

            end = time.time()
            params = '|'.join(['{:^4}'.format(param) for param in dir.split('_')])
            print('{:3}) {} || {}'.format(counter, params, end-start))
            counter += 1