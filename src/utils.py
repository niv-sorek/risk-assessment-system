import argparse
import json
import requests

from src.resources import Constants
from src.models.Fix import Fix
from src.models.Vulnerability import Vulnerability


def vulnerabilities_from_json_file(file_name):
    with open(file_name, 'r') as file:
        response_json = json.loads(file.read())
    return generate_vulnerabilities_list(response_json)


def find_vulnerabilities_from_api(vendor, product="", version=""):
    # Define arguments for API script
    parser = argparse.ArgumentParser()
    parser.add_argument('--recent', dest='recent', default=5, type=int)
    parser.add_argument('--details', dest='details', default=1, type=int)
    parser.add_argument('--id', dest='id')
    args = parser.parse_args()

    # Add your personal API key here
    personal_api_key = Constants.vuldb_api_key

    # Set HTTP Header
    user_agent = 'Niv and Lir'
    headers = {'User-Agent': user_agent, 'X-VulDB-ApiKey': personal_api_key}
    post_data = {"advancedsearch": "vendor:" + vendor + ",product:" + product + ",version:" + version,
                 "details": "1"}
    # URL VulDB endpoint
    url = 'https://vuldb.com/?api'
    response = requests.post(url, headers=headers, data=post_data)

    response_json = json.loads(response.content)
    v_list = generate_vulnerabilities_list(response_json)
    # with open(Constants.db_file_name, 'w') as file:
    #     for v in v_list:
    #         json.dump(v.__dict__, file)
    return v_list


def generate_vulnerabilities_list(source_json):
    vulnerabilities = []
    # result►0►countermeasure►upgrade►version

    for i in source_json['result']:
        cvss_key = i['vulnerability'].get('cvss2', None)
        if not cvss_key:
            cvss_key = i['vulnerability'].get('cvss3', None)
        if not cvss_key:
            level = 0
        else:
            level = cvss_key['nvd'].get('basescore', 0)
        countermeasure = i['countermeasure']
        name = countermeasure.get('name', "")
        if name != "":
            value = -1
            if name == "Patch":
                value = countermeasure['date']
            elif name == "Upgrade":
                value = countermeasure['upgrade']['version']
            fix = Fix(name, value)

        cve = i['source']['cve'].get('id', "unknown")
        num_of_exploits = i['exploit'].get("availability", 0)
        v = Vulnerability(cve, fix, num_of_exploits, level)
        vulnerabilities.append(v)
    return vulnerabilities


def get_exploits_by_cve(cve):
    url = 'http://cve.circl.lu/api/cve/' + cve
    response = requests.get(url)
    response_json = json.loads(response.content)
    print(len(response_json.get('capnec', [])))


# get_exploits_by_cve('CVE-2020-5752')


def get_vulnerabilities(vendor, product, version):
    return find_vulnerabilities_from_api(vendor, product, version)


def get_component_vulnerabilities(component):
    # return get_vulnerabilities(component.vendor, component.product, component.version)
    return vulnerabilities_from_json_file('src/resources/json_file.json')
