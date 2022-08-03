#!/usr/bin/python

import io
import sys
import fcntl
import time
import copy
import string
from AtlasI2C import (
	 AtlasI2C
)
    
def get_devices():
    device = AtlasI2C()
    device_address_list = device.list_i2c_devices()
    device_list = []
    
    # pH 99
    # EC 100
    # RTD 101
    # PMP 102
    # PMP 103
    # PMP 104
    # PMP 105
    
    
    for i in device_address_list:
        device.set_i2c_address(i)
        response = device.query("I")
        try:
            moduletype = response.split(",")[1] 
            response = device.query("name,?").split(",")[1]
        except IndexError:
            print(">> WARNING: device at I2C address " + str(i) + " has not been identified as an EZO device, and will not be queried") 
            continue
        device_list.append(AtlasI2C(address = i, moduletype = moduletype, name = response))
    return device_list 
       
       
def main():
    
    device_list = get_devices()
    
    print(device_list)
      
    device = device_list[0]
    
    while True:

        delaytime = 5
        
        try:
            while True:
                for dev in device_list:
                    dev.write("R")
                time.sleep(delaytime)
                for dev in device_list:
                    print(dev.read())
            
        except KeyboardInterrupt:
            print("Continuous polling stopped")
    
                    
if __name__ == '__main__':
    main()