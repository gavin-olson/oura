#!/usr/bin/python

import argparse
import requests
import json
from datetime import date
from statistics import fmean
import pygal

parser=argparse.ArgumentParser()
parser.add_argument('-t', '--token', help='File containing API token', default='token')
parser.add_argument('--start', help='Date to begin request', type=lambda s: date.fromisoformat(s), default=date.today())
parser.add_argument('--end', help='Date to end request', type=lambda s: date.fromisoformat(s), default=date.today())
parser.add_argument('-s', '--min_samples', help='Minimum samples to plot sleep period', default=48)
args=parser.parse_args()

with open(args.token, 'r') as token_file:
    token=token_file.read().strip()

sleep_raw=json.loads(
    requests.request(
        'GET',
        'https://api.ouraring.com/v2/usercollection/sleep',
        headers={'Authorization': f"Bearer {token}"},
        params={
            'start_date': args.start.isoformat(),
            'end_date': args.end.isoformat()
        }
    ).text
)

#print(sleep_raw)

print('date, samples, computed_avg, supplied_avg')
chart = pygal.DateTimeLine(
    x_label_rotation=35,
    x_label_formatter=lambda dt: dt.astimezone(tz=None).isoformat()
)

sleep_rates=[]
for sleep_night in sleep_raw['data']:
    samples=[x for x in sleep_night['heart_rate']['items'] if x != None]
    if len(samples) >= args.min_samples:
        sleep_rate=fmean(samples)
        sleep_day=date.fromisoformat(sleep_night['day'])
        print(f"{sleep_day}, {len(samples)}, {sleep_rate}, {sleep_night['average_heart_rate']}")
        sleep_rates.append((sleep_day,sleep_rate))

chart.add('bpm', sleep_rates)
chart.add('start_med', [(date(2024,8,1), 60), (date(2024,8,1),120)])
chart.add('stop', [(date(2024,11,5), 60), (date(2024,11,5),120)])
chart.render_in_browser()


#sleep_raw.data[blah].day
#                    .heart_rate.interval
#                              .items[blah]
