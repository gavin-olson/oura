#!/usr/bin/python

import argparse
import requests
import json
from datetime import datetime
import pygal

parser=argparse.ArgumentParser()
parser.add_argument('-t', '--token', help='File containing API token', default='token')
parser.add_argument('--start', help='Date/time to begin request', type=lambda s: datetime.fromisoformat(s), default=datetime.now().date())
parser.add_argument('--end', help='Date/time to end request', type=lambda s: datetime.fromisoformat(s), default=datetime.now())
args=parser.parse_args()

with open(args.token, 'r') as token_file:
    token=token_file.read().strip()

heartrate_raw=json.loads(
    requests.request(
        'GET',
        'https://api.ouraring.com/v2/usercollection/heartrate',
        headers={'Authorization': f"Bearer {token}"},
        params={
            'start_datetime': args.start.isoformat(),
            'end_datetime': args.end.isoformat()
        }
    ).text
)
        
heartrate=[{'timestamp': datetime.fromisoformat(x['timestamp']).astimezone(tz=None), 'source': x['source'], 'bpm': x['bpm']} for x in heartrate_raw['data']]

chart = pygal.DateTimeLine(
    x_label_rotation=35,
    x_label_formatter=lambda dt: dt.astimezone(tz=None).isoformat()
)
for source in {'awake', 'rest', 'workout'}:
    chart.add(source, [(x['timestamp'], x['bpm']) for x in heartrate if x['source']==source])
#chart.add('bpm', [(x['timestamp'], x['bpm']) for x in heartrate])
chart.render_in_browser()

