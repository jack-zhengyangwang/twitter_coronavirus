#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags',nargs='+',required=True)
parser.add_argument('--input_dir',default='outputs')
parser.add_argument('--output_path',default='alternative_reduce.png')
args = parser.parse_args()

# imports
import os
import re
import json
import datetime
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import font_manager

# use a font that has Korean/CJK characters if it has been downloaded
font_path = os.path.expanduser('~/.fonts/NanumGothic-Regular.ttf')
if os.path.exists(font_path):
    font_manager.fontManager.addfont(font_path)
    name = font_manager.FontProperties(fname=font_path).get_name()
    plt.rcParams['font.family'] = name

# scan the .lang outputs (one file per day) and count each hashtag per day
pattern = r'geoTwitter(\d\d)-(\d\d)-(\d\d)\.zip\.lang$'
counts = defaultdict(dict)
for filename in sorted(os.listdir(args.input_dir)):
    match = re.match(pattern, filename)
    if not match:
        continue
    yy, mm, dd = match.groups()
    day = datetime.date(2000+int(yy), int(mm), int(dd))
    path = os.path.join(args.input_dir, filename)
    with open(path) as f:
        tmp = json.load(f)
    for hashtag in args.hashtags:
        total = sum(tmp.get(hashtag, {}).values())
        counts[hashtag][day] = total

# plot one line per hashtag
fig, ax = plt.subplots(figsize=(12,6))
for hashtag in args.hashtags:
    days = sorted(counts[hashtag])
    values = [counts[hashtag][d] for d in days]
    ax.plot(days, values, label=hashtag)
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.set_xlabel('day of the year (2020)')
ax.set_ylabel('number of tweets')
ax.set_title('Daily tweets per hashtag in 2020')
ax.legend()
plt.tight_layout()
plt.savefig(args.output_path)
print('saved', args.output_path)
