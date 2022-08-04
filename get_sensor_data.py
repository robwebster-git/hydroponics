#!/usr/bin/python

import io
import sys
import fcntl
import time
import copy
import string
from datetime import datetime

sys.path.append('/home/pi/Raspberry-Pi-sample-code')

from AtlasI2C import (
	 AtlasI2C
)

address_to_name={
    99: 'pH',
    100: 'EC',
    101: 'RTD',
    102: 'PMP102',
    103: 'PMP103',
    104: 'PMP104',
    105: 'PMP105'
}
    
def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []
        
    for i in device_address_list:
        if i != 100: # restrict operation to only EC for now
            continue
        device.set_i2c_address(i)
        response = device.query("I")
        try:
            moduletype = response.split(",")[1] 
            response = device.query("name,?").split(",")[1]
        except IndexError:
            #print(">> WARNING: device at I2C address " + str(i) + " has not been identified as an EZO device, and will not be queried") 
            continue
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list 
       
       
def main():
    
    device_list = get_devices()
    delaytime = 2
    
    try:
        for dev in device_list:
            dev.write("R")
        time.sleep(delaytime)
        for dev in device_list:
            if dev.address != 100: # restrict operation to EC sensor for now
                print(f'Not 100: {dev.address}')
                continue
            name = address_to_name[dev.address]
            result = dev.read().strip().split(":")[-1].strip()
            with open(f'data_{name}_address_{dev.address}.csv', 'a+') as dd:
                dd.write(f'{datetime.now().strftime("%d-%m-%Y,%H:%M:%S")},{result}\n')                
                print(dev.address, name, result)
        
    except KeyboardInterrupt:
        print("Continuous polling stopped")
        sys.exit()
    
                    
if __name__ == '__main__':
    main()
