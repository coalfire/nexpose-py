#!/usr/bin/env python3

"""
Python3 bindings for the Nexpose API v3
"""
from collections import namedtuple
from datetime import datetime, timedelta
import urllib3

import requests

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


def nsclogin(*, base_url, user, password, verify=True):
    """
    Accept named args base_url, username, password (strings),
    optionally verify (Boolean default True).
    Return a named tuple used for Nexpose login.
    """
    l = namedtuple("Login", ['base_url', 'user', 'password', 'verify'])
    return l(base_url=base_url, user=user, password=password, verify=verify)


def get(*, login, endpoint, params=[]):
    """
    Accept named args login (nexpose.login), endpoint (string), optional params.
    Return get against nexpose.
    """
    url = f"{login.base_url}/{endpoint}"
    head = {"Accept": "application/json"}
    response = requests.get(
        url,
        auth=(login.user, login.password),
        headers=head,
        verify=login.verify,
        params=params
    )
    _require_response_200_ok(response)

    return response.json()


def delete(*, login, endpoint):
    """
    Accept named args login (nexpose.login) and endpoint (string)
    Return delete against nexpose.
    """
    url = f"{login.base_url}/{endpoint}"
    head = {"Accept": "application/json"}
    response = requests.delete(
        url, auth=(login.user, login.password), headers=head, verify=login.verify
    )
    _require_response_200_ok(response)

    return response.json()


def put(*, login, endpoint, data=[]):
    """
    Accept named args login (nexpose.login) and endpoint (string)
    Return put against nexpose.
    """
    url = f"{login.base_url}/{endpoint}"
    head = {"Accept": "application/json"}
    response = requests.put(
        url, auth=(login.user, login.password), headers=head, verify=login.verify, data=data,
    )
    _require_response_200_ok(response)

    return response.json()


def engines(login):
    """
    Accept login (nexpose.login).
    Return scan engines resources.
    """
    return get(login=login, endpoint="api/3/scan_engines")['resources']


def engine_pools(login):
    """
    Accept login (nexpose.login).
    Return pools resources.
    """
    return get(login=login, endpoint="api/3/scan_engine_pools")['resources']


def reports(*, login, page=0, size=10):
    """
    Accept named args login (nexpose.login), page, size (int).
    Return paginated reports response.
    """
    params = {'page': page, 'size': size}
    return get(login=login, endpoint="api/3/reports", params=params)


def report_history(*, login, report_id):
    """
    Accept named args login (nexpose.login), report_id (int).
    Return report history reponse.
    """
    return get(login=login, endpoint=f"api/3/reports/{report_id}/history")


def delete_report(*, login, report_id):
    """
    Accept named args login (nexpose.login), report_id (int).
    Return deleted report response.
    """
    return delete(login=login, endpoint=f"api/3/reports/{report_id}")


def scans(*, login, page=0, size=10):
    """
    Accept named args login (nexpose.login), page, size (int).
    Return paginated scans response.
    """
    params = {'page': page, 'size': size}
    return get(login=login, endpoint="api/3/scans", params=params)


def sites(*, login, page=0, size=10):
    """
    Accept named args login (nexpose.login), page, size (int).
    Return paginated sites response.
    """
    params = {'page': page, 'size': size}
    return get(login=login, endpoint="api/3/sites", params=params)


def site(*, login, site_id):
    """
    Accept named args login (nexpose.login), site_id (int).
    Return site response.
    """
    return get(login=login, endpoint=f"api/3/sites/{site_id}")


def site_id_older_than(*, login, site_id, days=90):
    """
    Accept named args login (nexpose.login), site_id (int),
    optional days (int, default 90).
    Return True is site is older than days,
    otherwise return False
    """
    now = datetime.now()
    max_age = timedelta(days=days)
    start_dates = [
        schedule['start']
        for schedule in schedules(login=login, site_id=site_id)
    ]
    if len(start_dates) == 0:
        return True
    for date in start_dates:
        # Nexpose date example:
        # '2020-11-01T11:22:27Z'
        print(date)
        start_time = datetime.strptime(date, '%Y-%m-%dT%H:%M:%SZ')
        if now - start_time < max_age:
            return False
    return True


def delete_site(*, login, site_id):
    """
    Accept named args login (nexpose.login), site_id (int).
    Return deleted site response.
    """
    return delete(login=login, endpoint=f"api/3/sites/{site_id}")


def schedules(*, login, site_id):
    """
    Accept named args login (nexpose.login), site_id (int).
    Return schedules resources.
    """
    return get(login=login, endpoint=f"api/3/sites/{site_id}/scan_schedules")['resources']


def assets(*, login, page=0, size=10):
    """
    Accept named args login (nexpose.login), page, size (int).
    Return paginated assets response.
    """
    params = {'page': page, 'size': size}
    return get(login=login, endpoint="api/3/assets", params=params)


def create_role(*, login, role):
    """
    Accept named args login (nexpose.login), role (dict).
    Return created role response.
    """
    return put(login=login, endpoint=f"api/3/roles/{role['id']}", data=role)
