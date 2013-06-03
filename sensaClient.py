#!/usr/bin/env python

import serial
import json
import requests
import time
import logging
import network
import sys 

# sampling interval in seconds
delay = 5 * 60

# feeds url
devs_url = 'http://sensa.herokuapp.com/api/devices/' 
moist_feed = devs_url + '50ff6c26011a940200000001'
humi_feed = devs_url + '5106def5b183c00200000001'
temp_feed = devs_url + '5106defcb183c00200000002'

# headers used by each request
headers = {'content-type': 'application/json',
           'Authorization': 'Token token="ZsJ3ND3UHpYx8pqYp1pqzg"'}

# logging configuration
logging.basicConfig(
    filename='/home/pi/logs/sensaClient.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s.'
)
logging.info('Posting data every %s seconds', delay)

# device initialization (arduino)
try:
    ardu = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
except serial.SerialException:
    logging.error('Device can not be found or can not be configured.')
    print 'ERROR : Device can not be found or can not be configured.'
    sys.exit(1)
time.sleep(2)

# read values from serial port and posts it to API
def take_sample():
    ardu.write('1')
    line = ardu.readline()
    humi, temp, moist = line.split(',')
    humi = {'value': int(float(humi.strip()))}
    temp = {'value': int(float(temp.strip()))}
    moist = {'value': float(moist.strip())}
    try:
        r = requests.post(humi_feed, data=json.dumps(humi), headers=headers)
	      if (r.status_code != 201): logging.error(r.text)
    except requests.exceptions.RequestException:
        network.restart()
    try:
        r = requests.post(temp_feed, data=json.dumps(temp), headers=headers)
	      if (r.status_code != 201): logging.error(r.text)
    except requests.exceptions.RequestException:
        network.restart()
    try:
        r = requests.post(moist_feed, data=json.dumps(moist), headers=headers)
    except requests.exceptions.RequestException:
	      if (r.status_code != 201): logging.error(r.text)
        network.restart()

while True:
    take_sample()
    time.sleep(delay)
