#!/bin/bash

UPDATE_SCRIPT_DIR=/home/pi
SENSOR_SCRIPTS_DIR=/home/pi/hydroponics
LOG=/home/pi/sensor_update.log

source /home/pi/envs/pi/bin/activate

python $SENSOR_SCRIPTS_DIR/get_dht22_temperature_data.py >> $LOG
sleep 3
python $SENSOR_SCRIPTS_DIR/get_dht22_humidity_data.py >> $LOG
sleep 3
python $SENSOR_SCRIPTS_DIR/get_ec_data.py >> $LOG
sleep 3
python $SENSOR_SCRIPTS_DIR/get_mh_z19b_data.py >> $LOG
sleep 3
python $SENSOR_SCRIPTS_DIR/get_pt1000_data.py >> $LOG
sleep 3
python $UPDATE_SCRIPT_DIR/update_remote_repo.py >> $UPDATE_SCRIPT_DIR/update_remote_repo.log
