import argparse
import json

import requests

from Venerability import Venerability


def find_vulnerabilities_from_file(file, search_term):
    with open(file) as file:
        response_json = json.loads(file.read())
    __find_vulnerabilities(response_json, search_term)


def find_vulnerabilities_from_API( search_term):
    # Define arguments for API script
    parser = argparse.ArgumentParser()
    parser.add_argument('--recent', dest='recent', default=5, type=int)
    parser.add_argument('--details', dest='details', default=0, type=int)
    parser.add_argument('--id', dest='id')
    args = parser.parse_args()

    # Add your personal API key here
    personalApiKey = '8076d3b1a1e2401d4d6e0df824b2d346'

    # Set HTTP Header
    userAgent = 'Email DLP System'
    headers = {'User-Agent': userAgent, 'X-VulDB-ApiKey': personalApiKey}
    post_data = {'search': search_term}
    # URL VulDB endpoint
    url = 'https://vuldb.com/?api'
    response = requests.post(url, headers=headers, data=post_data)

    response_json = json.loads(response.content)

    __find_vulnerabilities(response_json, search_term)


def __find_vulnerabilities(source_json, search_term):

    # Get API response

    # Output
    for i in source_json['result']:
        level = i['vulnerability']['risk'].get('value', 0)
        # level = i['vulnerability']['risk']['value']
        cve = i['source']['cve'].get('id', "unknown")
        # if level:
        #     print(cve, "Level: ", level)
        v = Venerability(cve, [], 2)
        print(v.venerability_name)
