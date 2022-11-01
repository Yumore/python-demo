#!/usr/bin/env python3
import json
import os

import requests
from jq import jq

__author__ = "Corsin Camichel"
__copyright__ = "Copyright 2020, Corsin Camichel"
__license__ = "Creative Commons Attribution-ShareAlike 4.0 International License."
__version__ = "1.0"
__email__ = "cocaman@gmail.com"

JQ_QUERY = ".data[].sha256_hash"

if __name__ == '__main__':
    data = {'query': 'get_recent', 'selector': "time"}
    response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=15)
    json_response = response.content.decode("utf-8", "ignore")
    json_response = json.loads(json_response)

    if (json_response["query_status"] == 'no_results'):
        print(f"No samples found, terminating.")
        quit()
    response = jq(JQ_QUERY).transform(json_response, multiple_output=True)

    for sample_sha256 in response:
        if (os.path.isfile(sample_sha256 + '.json') == False):
            data = {'query': 'get_info', 'hash': sample_sha256}
            response = requests.post('https://mb-api.abuse.ch/api/v1/', data=data, timeout=15, allow_redirects=True)
            open(sample_sha256 + '.json', 'wb').write(response.content)
