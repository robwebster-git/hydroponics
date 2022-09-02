import io
import sys
import fcntl
import time
import copy
import string
import json

sys.path.append('/home/pi/Raspberry-Pi-sample-code')

from AtlasI2C import AtlasI2C

import output_file

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
    
    for dev in device_list:
        if dev.address == 100: # restrict to only EC sensor for now
            dev.write("R")
            time.sleep(delaytime)
            name = address_to_name[dev.address]
            result = dev.read().strip().split(":")[-1]
            result = json.dumps(result).replace(r'\u0000', '').replace('"', '').strip()
            result = int(result)
            output_json = f'{output_file.OUTPUT_REPO_DIR}/{name}/data_{name}_{output_file.monthstamp}.json'
            df = output_file.add_datapoint_to_json(output_json, result)
            print(f'{name}: Added {result} to {output_json}')
            df.to_json(output_json)

if __name__ == '__main__':
    main()
