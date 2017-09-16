#!/usr/bin/python3
import argparse
import sys


"""
Test script to test the various features of test
"""

parser = argparse.ArgumentParser(description='Test executable for testuite')
parser.add_argument('-m', '--multiplication', action='store_true', help='Multiplication mode', required=False)

args = parser.parse_args()

op = lambda x, y: x + y
output = 0

if args.multiplication:
    op = lambda x, y: x * y
    output = 1

for line in sys.stdin:
    for num in line.split():
        output = op(output, int(num))

print(output)

