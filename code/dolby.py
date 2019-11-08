#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#******************************************************************************

# This program is protected under international and U.S. copyright laws as

# an unpublished work. This program is confidential and proprietary to the

# copyright owners. Reproduction or disclosure, in whole or in part, or the

# production of derivative works therefrom without the express permission of

# the copyright owners is prohibited.

#

#                Copyright (C) 2019 by Dolby Laboratories.

#                            All rights reserved.

#******************************************************************************/

 

import os

import json

import time

import logging

import requests

 

MAX_WAIT = 50

 

def job_start(key, uri, input_file, output_file, more={}):

    """

    POST file to begin a new job for a given URI endpoint

    """

    body = {

            'input' : input_file,

            'output': output_file,

        }

    body.update(more)

 

    headers = {
        'x-apikey': key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }

 

    logging.info("Request: {} {} {}".format(uri, headers, body))

 

    response = requests.post(uri, json=body, headers=headers)

    data = response.json()

 

    logging.info("Response: {}".format(json.dumps(data, indent=4,

        sort_keys=True)))

 

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(json.dumps(data, indent=4, sort_keys=True))
        print(err)
        raise
        
    return data

 

def job_result(key, uri, job_id, wait=0, noretry=False):

    """
    GET job result for a given URI endpoint
    """

    params = {
        'job_id' : job_id,
        }

 

    headers = {
        'x-apikey': key,
        'Content-Type': 'application/json',
        'Accept': 'application/json'
        }

 

    logging.info("Request: {} {} {}".format(uri, headers, params))
    response = requests.get(uri, params=params, headers=headers)
    logging.info("Response: {} {}".format(response.status_code, response.content))

 

    if response.status_code == 200:
        data = response.json()

 

        if noretry:
            return data

 

        # Retry with progressive backoff while job is being worked on

        if 'status' in data and data['status'] in ['Pending', 'Running']:

            # Limit how long and how many attempts we'll make

            if wait > MAX_WAIT:

                raise ValueError("Giving up after multiple attempts")

 

            wait = wait + 1

            logging.info("Job Pending - waiting {}".format(wait))

            time.sleep(wait)

            print('.')

            return job_result(key, uri, job_id, wait=wait)

 

        return data

    else:

        print(job_id)

 

    response.raise_for_status()

def run(api, key, url, input_file, output_file, more={}):

    result = job_start(key, url + api, input_file, output_file, more=more)

    job_id = result['job_id']

    print(job_id)

 

    data = job_result(key, url + api, job_id)

    print(json.dumps(data, indent=4, sort_keys=True))

#     Capturing audio can pick up a variety of noises that distract from the dialog the listener 
#     wants to focus on.  The Noise Processing API helps you fix audio recorded in noisy 
#     environments or with poor equipment to create consistency across your recordings.
    
def noise(key, url, input_file, output_file, more={}):
    api = '/beta/media/process/noise'
    run(api, key, url, input_file, output_file, more=more)


#  To create studio sound for the dialog in your recorded audio, it is useful to detect and reduce the
#     sibilance captured by the microphone.  This is a characteristic of harsh consonant sounds 
#     like "s", "sh", "x", "ch", "t", and "th".  A de-esser can help reduce listener fatigue 
#     from this sometimes whistling sound coming from the over-pronunciation of certain language.

def sibilance(key, url, input_file, output_file, more={}):
    api = '/beta/media/process/sibilance'
    run(api, key, url, input_file, output_file, more=more)

#     In order to give your audio more presence and authority it is valuable to modify the tone.  
#     The Tone Processing API will help with equalization to shape the audio from your recorded 
#     files to match a listener profile.
def tone(key, url, input_file, output_file, more={}):
    api = '/beta/media/process/tone'
    run(api, key, url, input_file, output_file, more=more)


if __name__ == '__main__':

    noise('…', 'https://api.dolby.com', '~/input.wav', '~/output.wav')
    sibilance('…', 'https://api.dolby.com', '~/input.wav', '~/output.wav')
    tone('…', 'https://api.dolby.com', '~/input.wav', '~/output.wav')

