"""
Get Nexpose user and password from environment or prompt
"""

import getpass

from os import environ


def user(credentials):
    """
    Return user (string), taken from environment, credential file, or prompt
    """
    try:
        nexpose_user = environ["NEXPOSE_USER"]
    except KeyError:
        try:
            nexpose_user = yaml.load(open(credentials))['username']
        except [FileNotFoundError, TypeError, KeyError]:
            nexpose_user = getpass.getpass(prompt="Nexpose user:")

    return nexpose_user


def password(credentials):
    """
    Return key (string), taken from environment, credential file, or prompt
    """
    try:
        nexpose_password = environ["NEXPOSE_PASS"]
    except KeyError:
        try:
            nexpose_password = yaml.load(open(credentials))['password']
        except [FileNotFoundError, TypeError, KeyError]:
            nexpose_password = getpass.getpass(prompt="Nexpose password:")
    return nexpose_password
