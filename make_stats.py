#!/usr/bin/env python

import json

with open('statistics.json', 'r') as stats_file:
    data = json.load(stats_file)
    for call in data.keys():
        if len(data[call].keys()) >= 3:
            qso_count = 0
            for country in data[call].keys():
                for band in data[call][country].keys():
                    qso_count += len(set(data[call][country][band]))
            if qso_count >= 6:
                print(call, qso_count)