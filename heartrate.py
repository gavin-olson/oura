#!/usr/bin/python

import requests
import json
from datetime import datetime
import pygal

with open('token', 'r') as token_file:
    token=token_file.read().strip()

heartrate_raw=json.loads(
    requests.request(
        'GET',
        'https://api.ouraring.com/v2/usercollection/heartrate',
        headers={'Authorization': f"Bearer {token}"},
        params={
            'start_datetime': '2024-12-27T00:00:00-05:00',
            'end_datetime': '2024-12-27T23:59:59-05:00'
        }
    ).text
)
        
heartrate=[{'timestamp': datetime.fromisoformat(x['timestamp']), 'source': x['source'], 'bpm': x['bpm']} for x in heartrate_raw['data']]

chart = pygal.DateTimeLine()
for source in {'awake', 'rest', 'workout'}:
    chart.add(source, [(x['timestamp'], x['bpm']) for x in heartrate if x['source']==source])
chart.render_to_file('heartrate.svg')

