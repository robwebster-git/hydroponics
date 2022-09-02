#!/usr/bin/python3
import sys

import pandas as pd
from pigpio_dht import DHT22

import output_file

# Read from DHT22 sensor
# Example output: {'temp_c': 23.7, 'temp_f': 74.7, 'humidity': 56.1, 'valid': True}

gpio = 4
sensor = DHT22(gpio)
name = 'DHT22_temperature'

try:
    response = sensor.read()
    valid = response['valid']
    result = response['temp_c']
except TimeoutError as timeout_error:
    sys.exit(f'{name}: Sensor read attempt failed due to timeout.  Another attempt will be made when the script next runs')

if valid:
    output_json = f'{output_file.OUTPUT_REPO_DIR}/{name}/{name}_{output_file.monthstamp}.json'
    df = output_file.add_datapoint_to_json(output_json, result)
    print(f'{name}: Added {result} to {output_json}')
    df.to_json(output_json)
