#!/usr/bin/python3
import os
import sys
from datetime import datetime as dt

import pandas as pd

OUTPUT_REPO_DIR='/home/pi/hydroponics'

# Get datetime stamp
now = dt.now()
datestamp = f'{now.year}-{str(now.month).zfill(2)}-{str(now.day).zfill(2)}T{str(now.hour).zfill(2)}:{str(now.minute).zfill(2)}'
monthstamp = f'{now.year}{str(now.month).zfill(2)}'

# Build output
def add_datapoint_to_json(output_json, value):  
    if os.path.exists(output_json):
        df = pd.read_json(output_json)
    else:
        df = pd.DataFrame(columns={'datestamp', 'value'})
    new_record = pd.DataFrame.from_records({'datestamp': [datestamp],'value': [value]})
    df = pd.concat([df, new_record], ignore_index=True, axis=0)

    return df

