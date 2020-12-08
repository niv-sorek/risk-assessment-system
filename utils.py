import argparse
import json

import requests

import Constants
from Venerability import Venerability


def find_vulnerabilities_from_file(file, search_term):
    with open(file) as file:
        response_json = json.loads(file.read())
    __find_vulnerabilities(response_json, search_term)


def find_vulnerabilities_from_api(search_term):
    # Define arguments for API script
    parser = argparse.ArgumentParser()
    parser.add_argument('--recent', dest='recent', default=5, type=int)
    parser.add_argument('--details', dest='details', default=0, type=int)
    parser.add_argument('--id', dest='id')
    args = parser.parse_args()

    # Add your personal API key here
    personal_api_key = Constants.vuldb_api_key

    # Set HTTP Header
    user_agent = 'Email DLP System'
    headers = {'User-Agent': user_agent, 'X-VulDB-ApiKey': personal_api_key}
    post_data = {'search': search_term}
    # URL VulDB endpoint
    url = 'https://vuldb.com/?api'
    response = requests.post(url, headers=headers, data=post_data)

    response_json = json.loads(response.content)

    __find_vulnerabilities(response_json, search_term)


def __find_vulnerabilities(source_json, search_term):
    # Get API response

    # Output
    vuls = []
    for i in source_json['result']:
        level = i['vulnerability']['risk'].get('value', 0)
        # level = i['vulnerability']['risk']['value']
        cve = i['source']['cve'].get('id', "unknown")
        # if level:
        #     print(cve, "Level: ", level)
        v = Venerability(cve, [], 2)
        vuls.append(v)
    return vuls
