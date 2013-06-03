#!/usr/bin/env python

import serial
import json
import requests
import time
import logging
import network

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

# device initialization (arduino)
ardu = serial.Serial("/dev/ttyACM0", 9600)
time.sleep(2)

# logging configuration
logging.basicConfig(
    filename='/home/pi/logs/sensaClient.log',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s.'
)
logging.info('Posting data every %s seconds', delay)

while True:
    ardu.write('1')
    line = ardu.readline()
    humi, temp, moist = line.split(',')
    humi = {'value': int(float(humi.strip()))}
    temp = {'value': int(float(temp.strip()))}
    moist = {'value': float(moist.strip())}
    try:
        requests.post(humi_feed, data=json.dumps(humi), headers=headers)
    except requests.exceptions.RequestException:
        network.restart()
    try:
        requests.post(temp_feed, data=json.dumps(temp), headers=headers)
    except requests.exceptions.RequestException:
        network.restart()
    try:
        requests.post(moist_feed, data=json.dumps(moist), headers=headers)
    except requests.exceptions.RequestException:
        network.restart()
    time.sleep(delay)
