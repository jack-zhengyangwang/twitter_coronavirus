#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict
import matplotlib.pyplot as plt

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
key = []
value = []
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items[:10][::-1]:
    key.append(k)
    value.append(v)

# plot bar chart for top 10 country
plt.bar(key, value)
plt.xlabel('language or country')
plt.ylabel('number of tweets')
plt.title('Tweets with ' + args.key)
plt.savefig(args.input_path + '_' + args.key + '.png')
