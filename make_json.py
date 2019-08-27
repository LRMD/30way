#!/usr/bin/env python
import re
import json
import collections

def get_fields(adif_file, field_name):
    adif_fh = open(adif_file, 'r')
    log = adif_fh.readlines()
    pattern = re.compile('^.*<' + field_name + ':\d+>([^<]*)<.*$', re.IGNORECASE)
    matches = [re.match(pattern, line) for line in log]
    adif_fh.seek(0)
    return [line[1].strip() for line in matches if line is not None]

calls = collections.defaultdict(dict)
adif = {}

for country in ['ES', 'YL', 'LY']:
    adif[country] = {}
    for item in ['call', 'band', 'mode']:
        adif[country][item + 's'] = get_fields(country + '30WAY.adi', item)

    for participant in adif[country]['calls']:
        if participant not in calls.keys():
            calls[participant] = {}
        calls[participant][country] = collections.defaultdict(list)
        qso_index = [i for i, x in enumerate(adif[country]['calls']) if x == participant]
        for qso in qso_index:
            calls[participant][country][adif[country]['bands'][qso]].append(
                adif[country]['modes'][qso]
            )

json_data = json.dumps(calls, indent=2)
json_file = open("statistics.json", "w+")
json_file.write(json_data)
json_file.close()
