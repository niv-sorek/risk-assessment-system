import json
import pathlib
import urllib

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
    post_data = {"advancedsearch": f"vendor:{vendor},product:{product}",
                 "details": "0",
                 'fields': "entry_details_countermeasure, countermeasure_upgrade_version, countermeasure_patch_name"}
    if len(version) > 0:
        post_data['advancedsearch'] += f", version:{version}"
    # URL VulDB endpoint
    url = 'https://vuldb.com/?api'
    response = requests.post(url, headers=headers, data=post_data)
    response_json = json.loads(response.content)
    print(response_json)
    # cves = []
    # for i in response_json['result']:
    #     cves.append(i['source']['cve']['id'])
    # vul_json = []
    # for cve in cves:
    #     with urllib.request.urlopen(
    #             f"https://raw.githubusercontent.com/olbat/nvdcve/master/nvdcve/{cve}.json") as url:
    #         vul_json.append(json.loads(url.read().decode()))

    vul_json = [json.loads("""{
  "cve": {
    "data_type": "CVE",
    "data_format": "MITRE",
    "data_version": "4.0",
    "CVE_data_meta": {
      "ID": "CVE-2020-0044",
      "ASSIGNER": "cve@mitre.org"
    },
    "problemtype": {
      "problemtype_data": [
        {
          "description": [
            {
              "lang": "en",
              "value": "CWE-125"
            }
          ]
        }
      ]
    },
    "references": {
      "reference_data": [
        {
          "url": "https://source.android.com/security/bulletin/2020-03-01",
          "name": "https://source.android.com/security/bulletin/2020-03-01",
          "refsource": "MISC",
          "tags": [
            "Vendor Advisory"
          ]
        }
      ]
    },
    "description": {
      "description_data": [
        {
          "lang": "en",
          "value": "In set_nonce of fpc_ta_qc_auth.c, there is a possible out of bounds read due to a missing bounds check. This could lead to local information disclosure with System execution privileges needed. User interaction is not needed for exploitation.Product: AndroidVersions: Android kernelAndroid ID: A-137650219"
        }
      ]
    }
  },
  "configurations": {
    "CVE_data_version": "4.0",
    "nodes": [
      {
        "operator": "OR",
        "cpe_match": [
          {
            "vulnerable": true,
            "cpe23Uri": "cpe:2.3:o:google:android:-:*:*:*:*:*:*:*"
          }
        ]
      }
    ]
  },
  "impact": {
    "baseMetricV3": {
      "cvssV3": {
        "version": "3.1",
        "vectorString": "CVSS:3.1/AV:L/AC:L/PR:H/UI:N/S:U/C:H/I:N/A:N",
        "attackVector": "LOCAL",
        "attackComplexity": "LOW",
        "privilegesRequired": "HIGH",
        "userInteraction": "NONE",
        "scope": "UNCHANGED",
        "confidentialityImpact": "HIGH",
        "integrityImpact": "NONE",
        "availabilityImpact": "NONE",
        "baseScore": 4.4,
        "baseSeverity": "MEDIUM"
      },
      "exploitabilityScore": 0.8,
      "impactScore": 3.6
    },
    "baseMetricV2": {
      "cvssV2": {
        "version": "2.0",
        "vectorString": "AV:L/AC:L/Au:N/C:P/I:N/A:N",
        "accessVector": "LOCAL",
        "accessComplexity": "LOW",
        "authentication": "NONE",
        "confidentialityImpact": "PARTIAL",
        "integrityImpact": "NONE",
        "availabilityImpact": "NONE",
        "baseScore": 2.1
      },
      "severity": "LOW",
      "exploitabilityScore": 3.9,
      "impactScore": 2.9,
      "acInsufInfo": false,
      "obtainAllPrivilege": false,
      "obtainUserPrivilege": false,
      "obtainOtherPrivilege": false,
      "userInteractionRequired": false
    }
  },
  "publishedDate": "2020-03-10T20:15Z",
  "lastModifiedDate": "2020-03-11T15:58Z"
}""")]
    v_list = generate_vulnerabilities_list(vul_json)
    return v_list


def generate_vulnerabilities_list(vul_json):
    vulnerabilities = []
    if len(vul_json) > 0:
        for vulnerability in vul_json:
            cve = vulnerability['cve']['CVE_data_meta'].get('ID', "unknown")
            E, AC, AV, RL, UI, PR = _get_vulnerability_cvss_metrics(vulnerability)
            fix = _get_vulnerability_fix(vulnerability)
            vulnerabilities.append(Vulnerability(cve, fix, E, AC, AV, RL, UI, PR))
    return vulnerabilities


def _get_vulnerability_cvss_metrics(i):
    cvss_key = i['impact']['baseMetricV3'].get('cvssV3', None)
    if cvss_key is not None:
        vector = cvss_key['vectorString']
        split = vector.split('/')
        vec_dict = dict(item.split(":") for item in vector.split("/"))
        E = vec_dict.get('E', 1)
        AC = vec_dict.get('AC', 1)
        AV = vec_dict.get('AV', 1)
        RL = vec_dict.get('RL', 1)
        UI = vec_dict.get('UI', 1)
        PR = vec_dict.get('PR', 1)
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
