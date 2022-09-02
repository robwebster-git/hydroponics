import os
import sys
import pandas as pd

import mh_z19

import output_file

# Read from MH_Z19B sensor (UART) serial port /dev/ttyUSB0
# Example output: {'co2': 645}

mh_z19.set_serialdevice('/dev/ttyUSB0')

name='MH_Z19B'

try:
    result = mh_z19.read()['co2']
except TimeoutError as timeout_error:
    sys.exit(f'{name}: Sensor read attempt failed due to timeout.  Another attempt will be made when the script next runs')
else:
    output_json = f'{output_file.OUTPUT_REPO_DIR}/{name}/{name}_{output_file.monthstamp}.json'
    df = output_file.add_datapoint_to_json(output_json, result)
    print(f'{name}: Added {result} to {output_json}')
    df.to_json(output_json)

