"""
Senz Wifi Session
"""

import json
import requests
import os
import urllib3
from . import urls

def _validate_response(response):
    """ Verify that response is OK """
    if response.status_code == 200:
        return
    raise ResponseError(response.status_code, response.text)


class Error(Exception):
    ''' Senz Wifi session error '''
    pass

class RequestError(Error):
    ''' Wrapped requests.exceptions.RequestException '''
    pass


class LoginError(Error):
    ''' Login failed '''
    pass

class ResponseError(Error):
    ''' Unexcpected response '''
    def __init__(self, status_code, text):
        super(ResponseError, self).__init__(
            'Invalid response'
            ', status code: {0} - Data: {1}'.format(
                status_code,
                text))
        self.status_code = status_code
        self.text = text

class Session(object):
    """ Senz Wifi session

    Args:
        username (str): Username used to login to Senz Wifi
        password (str): Password used to login to Senz Wifi

    """

    def __init__(self, username, password, tokenFileName='~/.senz-wifi-token', raw=False, verifySsl=True):
        self._username = username
        self._password = password
        self._tokenFileName = os.path.expanduser(tokenFileName)
        self._sessionId = None
        self._raw = raw
        self._verifySsl = verifySsl


    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def login(self):
        """ Login to Senz Wifi """

        if os.path.exists(self._tokenFileName):
            with open(self._tokenFileName, 'r') as cookieFile:
                self._sessionId = cookieFile.read().strip()

            if self._raw: print("--- token found")

            try:
                self._get_groups()

            except ResponseError:
                if self._raw: print("--- token probably expired")

                self._sessionId = None
                self._devices = None
                os.remove(self._tokenFileName)

        if self._sessionId is None:
            self._create_session()
            with open(self._tokenFileName, 'w') as tokenFile:
                tokenFile.write(self._sessionId)

            self._get_groups()


    def logout(self):
        pass

    def _headers(self):
        return {
            "Accept": "application/json",
            "Content-Type": "application/json; charset=utf-8"
        }

    def _create_session(self):
        response = None

        if self._raw: print("--- creating session by authenticating")

        try:
            response = requests.get(urls.login(self._username, self._password), headers=self._headers(), verify=self._verifySsl)
            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)

        except requests.exceptions.RequestException as ex:
            raise LoginError(ex)

        _validate_response(response)

        if(self._raw is True):
            print("--- raw beginning ---")
            print(response.text)
            print("--- raw ending    ---\n")

        self._sessionId = json.loads(response.text)['SessionId']

    def _get_groups(self):
        """ Get information about groups """
        response = None

        try:
            response = requests.get(urls.get_groups(self._sessionId),headers=self._headers(), verify=self._verifySsl)

            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)

        except requests.exceptions.RequestException as ex:
            raise RequestError(ex)

        _validate_response(response)

        if(self._raw is True):
            print("--- _get_groups()")
            print("--- raw beginning ---")
            print(response.text)
            print("--- raw ending    ---\n")

        self._groups = json.loads(response.text)
     

    def get_devices(self):
        if self._sessionId is None:
            self.login()

        try:
            response = requests.get(urls.get_devices(self._sessionId),headers=self._headers(), verify=self._verifySsl)

            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)

        except requests.exceptions.RequestException as ex:
            raise RequestError(ex)

        _validate_response(response)

        if(self._raw is True):
            print("--- get_devices()")
            print("--- raw beginning ---")
            print(response.text)
            print("--- raw ending    ---\n")

        devices = []
        data = json.loads(response.text)
        for group in data['Groups']:
            for device in group['Thermostats']:
                devices.append({
                    'serial': device['SerialNumber'],
                    'name': device['Room'],
                    'group': device['GroupName']
                })
        return devices

    def get_device(self, serial):
        if self._sessionId is None:
            self.login()

        try:
            response = requests.get(urls.get_device(self._sessionId, serial),headers=self._headers(), verify=self._verifySsl)

            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)

        except requests.exceptions.RequestException as ex:
            raise RequestError(ex)

        _validate_response(response)

        if(self._raw is True):
            print(f"--- get_device({serial})")
            print("--- raw beginning ---")
            print(response.text)
            print("--- raw ending    ---\n")

        return json.loads(response.text)
    