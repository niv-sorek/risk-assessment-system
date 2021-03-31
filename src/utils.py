import json
import pathlib

import requests

from src.models.Fix import Fix
from src.models.Vulnerability import Vulnerability
from src.resources import Constants


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)


def vulnerabilities_from_json_file(file_name):
    with open(file_name, 'r') as file:
        response_json = json.loads(file.read())
    return generate_vulnerabilities_list(response_json)


def find_vulnerabilities_from_api(vendor, product="", version=""):
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
    print(response_json)
    v_list = generate_vulnerabilities_list(response_json)

    return v_list


def generate_vulnerabilities_list(source_json):
    vulnerabilities = []
    if source_json.get('result', None) is not None:
        for vulnerability in source_json['result']:
            cve = vulnerability['source']['cve'].get('id', "unknown")
            E, AC, AV, RL, UI, PR = _get_vulnerability_cvss_metrics(vulnerability)
            num_of_exploits = vulnerability['exploit'].get("availability", 0)
            fix = _get_vulnerability_fix(vulnerability)
            vulnerabilities.append(Vulnerability(cve, fix, num_of_exploits, E, AC, AV, RL, UI, PR))
    return vulnerabilities


def _get_vulnerability_cvss_metrics(i):
    cvss_key = i['vulnerability'].get('cvss3', None)
    E = cvss_key['nvd'].get('e', 0)
    AC =cvss_key['nvd'].get('ac', 0)
    AV = cvss_key['nvd'].get('av', 0)
    RL =cvss_key['nvd'].get('rl', 0)
    UI = cvss_key['nvd'].get('ui', 0)
    PR = cvss_key['nvd'].get('pr', 0)
    return E, AC, AV, RL, UI, PR


def _get_vulnerability_fix(vul_json):
    countermeasure = vul_json['countermeasure']
    name = countermeasure.get('name', "")
    if name != "":
        value = -1
        if name == "Patch":
            value = countermeasure['date']
        elif name == "Upgrade":
            value = countermeasure['upgrade']['version']
        fix = Fix(name, value)
        return fix
    return None


def _get_component_vulnerabilities(vendor, product, version):
    return find_vulnerabilities_from_api(vendor, product, version)


def get_component_vulnerabilities(component, from_api):
    if from_api:
        return _get_component_vulnerabilities(component.vendor, component.product, component.version)
    else:
        if component.product == 'mitalk':
            return vulnerabilities_from_json_file(pathlib.Path(__file__).parent / 'resources/json_file_xiaomi.json')
        elif component.vendor == 'microsoft':
            return vulnerabilities_from_json_file(pathlib.Path(__file__).parent / 'resources/json_file_microsoft.json')
        else:
            return vulnerabilities_from_json_file(pathlib.Path(__file__).parent / 'resources/json_file_xiaomi.json')
