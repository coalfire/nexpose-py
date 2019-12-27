#!/usr/bin/env python3

"""
Python3 bindings for the Nexpose API v3
"""

import requests
import urllib3
urllib3.disable_warnings()

class NexposeException(Exception):
    """
    Base class for exceptions in this module.
    """

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        print(self.status_code)
        print(self.message)


class ResponseNotOK(NexposeException):
    """
    Request did not return 200 (OK)
    """



def _require_response_200_ok(response):
    """
    Accept a requests.response object.
    Raise ResponseNotOK if status code is not 200.
    Otherwise, return True
    """
    if response.status_code != 200:
        raise ResponseNotOK(
            status_code=response.status_code, message=response.text
        )
    return True


def engines(*, base_url, user, password, verify=True):
    """
    Accept named args base_url, username, password (strings)
    Return scan engines.
    """
    url = base_url + "/api/3/scan_engines"
    head = {"Accept": "application/json"}
    response = requests.get(
        url, auth=(user, password), headers=head, verify=verify
    )
    _require_response_200_ok(response)

    return response.json()['resources']

def engine_pools(*, base_url, user, password, verify=True):
    """
    Accept named args base_url, username, password (strings)
    Return pools.
    """
    url = base_url + "/api/3/scan_engine_pools"
    head = {"Accept": "application/json"}
    response = requests.get(
        url, auth=(user, password), headers=head, verify=verify
    )
    _require_response_200_ok(response)

    return response.json()

def reports(*, base_url, user, password, verify=True, page=0, size=10):
    """
    Accept named args base_url, username, password (strings)
    Return reports response.
    """
    url = base_url + "/api/3/reports"
    head = {"Accept": "application/json"}
    params = {'page': page, 'size': size}
    response = requests.get(
        url, auth=(user, password), headers=head, verify=verify, params = params
    )
    _require_response_200_ok(response)

    return response.json()

def report_history(*, report_id, base_url, user, password, verify=True):
    """
    Accept named args report_id, base_url, username, password (strings)
    Return report history reponse.
    """
    url = base_url + "/api/3/reports/" + str(report_id) + "/history"
    head = {"Accept": "application/json"}
    response = requests.get(
        url, auth=(user, password), headers=head, verify=verify
    )
    _require_response_200_ok(response)

    return response.json()

def delete_report(*, report_id, base_url, user, password, verify=True):
    """
    Accept named args report_id, base_url, user, password (strings)
    Return deleted report response.
    """
    url = base_url + "/api/3/reports/" + str(report_id)
    head = {"Accept": "application/json"}
    response = requests.delete(
        url, auth=(user, password), headers=head, verify=verify
    )
    _require_response_200_ok(response)

    return response.json()

def scans(*, base_url, user, password, verify=True, page=0, size=10):
    """
    Accept named args base_url, username, password (strings)
    Return scans response.
    """
    url = base_url + "/api/3/scans"
    head = {"Accept": "application/json"}
    params = {'page': page, 'size': size}
    response = requests.get(
        url, auth=(user, password), headers=head, verify=verify, params = params
    )
    _require_response_200_ok(response)

    return response.json()

def sites(*, base_url, user, password, verify=True, page=0, size=10):
    """
    Accept named args base_url, username, password (strings)
    Return sites response.
    """
    url = base_url + "/api/3/sites"
    head = {"Accept": "application/json"}
    params = {'page': page, 'size': size}
    response = requests.get(
        url, auth=(user, password), headers=head, verify=verify, params = params
    )
    _require_response_200_ok(response)

    return response.json()

def site(*, site_id, base_url, user, password, verify=True):
    """
    Accept named args base_url, username, password (strings)
    Return site response.
    """
    url = base_url + "/api/3/sites" + str(site_id)
    head = {"Accept": "application/json"}
    response = requests.get(
        url, auth=(user, password), headers=head, verify=verify
    )
    _require_response_200_ok(response)

    return response.json()

def assets(*, base_url, user, password, verify=True, page=0, size=10):
    """
    Accept named args base_url, username, password (strings)
    Return assets response.
    """
    url = base_url + "/api/3/assets"
    head = {"Accept": "application/json"}
    params = {'page': page, 'size': size}
    response = requests.get(
        url, auth=(user, password), headers=head, verify=verify, params = params
    )
    _require_response_200_ok(response)

    return response.json()

def create_role(*, role, base_url, user, password, verify=True):
    """
    Accept named args role (hash), base_url, user, password (strings)
    Return created role response.
    """
    url = base_url + "/api/3/roles/" + role['id']
    head = {"Accept": "application/json"}
    response = requests.put(
        url, auth=(user, password), headers=head, verify=verify, data=role,
    )
    _require_response_200_ok(response)

    return response.json()
