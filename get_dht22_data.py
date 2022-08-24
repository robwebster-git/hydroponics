#!/usr/bin/python3
import os
import sys
from datetime import datetime as dt

import pandas as pd

from pigpio_dht import DHT22

# Read from DHT22 sensor
# Example output: {'temp_c': 23.7, 'temp_f': 74.7, 'humidity': 56.1, 'valid': True}
gpio = 4
sensor = DHT22(gpio)

try:
	result = sensor.read()
except TimeoutError as timeout_error:
	sys.exit('Sensor read attempt failed due to timeout.  Another attempt will be made when the script next runs')

# Get datetime stamp
now = dt.now()
datestamp = f'{now.year}{str(now.month).zfill(2)}{str(now.day).zfill(2)}_{str(now.hour).zfill(2)}{str(now.minute).zfill(2)}'
monthstamp = f'{now.year}{str(now.month).zfill(2)}'

# Build output
output_csv = f'/home/pi/hydroponics/DHT22_data/data_DHT22_GPIO4_{monthstamp}.csv'
output_json = f'/home/pi/hydroponics/DHT22_data/data_DHT22_GPIO4_{monthstamp}.json'

if os.path.exists(output_csv):
	df = pd.read_csv(output_csv)
else:
	df = pd.DataFrame(columns={'datestamp', 'dht22_temp', 'dht22_humidity'})
if result['valid']:
	new_record = pd.DataFrame.from_records({'datestamp': [datestamp],'dht22_temp': [result['temp_c']], 'dht22_humidity': [result['humidity']]})
	df = pd.concat([df, new_record], ignore_index=True, axis=0)

	# Write output
	df.to_csv(output_csv, index=False)
	df.to_json(output_json)
else:
	print("Invalid data, skipping")

