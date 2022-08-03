#!/bin/python3

import os
from datetime import datetime
import random
from git import Repo

REPO_DIR="/home/pi/dummy_sensor_data"

# Append latest "data"
with open(f'{REPO_DIR}/ph.csv', 'a+') as f:
    f.write(f'{datetime.now().strftime("%d-%m-%Y,%H-%M-%S")},{random.randint(30,100)/10}\n')

# Add, commit, push
repo = Repo(REPO_DIR)
repo.git.add(REPO_DIR)
repo.index.commit('Updated pH sensor data: {datetime.now().strftime("%d-%m-%Y-%H-%M-%S")')
repo.remotes.origin.push('main')

