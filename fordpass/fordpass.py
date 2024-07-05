import hashlib
import random
import string
import requests
import logging
import time

from .constants import (
    REGION_OPTIONS,
    REGIONS,
)
from base64 import urlsafe_b64encode


_LOGGER = logging.getLogger(__name__)

defaultHeaders = {
    'Accept': '*/*',
    'Accept-Language': 'en-us',
    "User-Agent": "FordPass/23 CFNetwork/1408.0.4 Darwin/22.5.0",
    'Accept-Encoding': 'gzip, deflate, br',
}

apiHeaders = {
    **defaultHeaders,
    'Application-Id': '71A3AD0A-CF46-4CCF-B473-FC7FE5BC4592',    
    'Content-Type': 'application/json',
}

baseUrl = 'https://usapi.cv.ford.com/api'

session = requests.Session()

class Vehicle(object):
    '''Represents a Ford vehicle, with methods for status and issuing commands'''

    def __init__(self, username, password, vin, region):
        self.username = username
        self.password = password
        self.vin = vin
        self.region = region
        self.token = None
        self.expires = None
        self.login_input = {}
    
    def auth(self):       
        '''Authenticate and store the token'''

        self.region_details = self.__region_details()
        _LOGGER.debug(f"region_details: {self.region_details}")

        initial_url = self.generate_url() 

        data = {
            'client_id': '9fb503e0-715b-47e8-adfd-ad4b7770f73b',
            'grant_type': 'password',
            'username': self.username,
            'password': self.password
        }

        headers = {
            **defaultHeaders,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

#        r = requests.post('https://fcis.ice.ibmcloud.com/v1.0/endpoint/default/token', data=data, headers=headers)
# GET
# https://login.ford.com/4566605f-43a7-400a-946e-89cc9fdb0bd7/B2C_1A_SignInSignUp_en-US/oauth2/v2.0/authorize?redirect_uri=fordapp://userauthorized&response_type=code&max_age=3600&code_challenge=meXP5e9rTz50hB4Ws20WqOrzi_I2H3SpVwJiiqWavQo&code_challenge_method=S256&scope=%2009852200-05fd-41f6-8c21-d36d3497dc64%20openid&client_id=09852200-05fd-41f6-8c21-d36d3497dc64&ui_locales=en-US&language_code=en-US&country_code=USA&ford_application_id=71A3AD0A-CF46-4CCF-B473-FC7FE5BC4592
        r = session.get(initial_url, headers=headers)
        _LOGGER.debug(f"r.status_code: {r.status_code}")
        # 'apparent_encoding', 'close', 'connection', 'content', 'cookies', 'elapsed', 'encoding', 'headers', 'history', 'is_permanent_redirect', 'is_redirect', 'iter_content', 'iter_lines', 'json', 'links', 'next', 'ok', 'raise_for_status', 'raw', 'reason', 'request', 'status_code', 'text', 'url']
        _LOGGER.debug(f"dir(r):: {dir(r)}")

        if r.status_code == 200:
# POST
# https://login.ford.com/4566605f-43a7-400a-946e-89cc9fdb0bd7/B2C_1A_SignInSignUp_en-US/SelfAsserted?tx=StateProperties=eyJUSUQiOiIzMzlkN2E0YS02MmNlLTQwNGEtYTU2My01YjI5ODdkZDMzZGYifQ&p=B2C_1A_SignInSignUp_en-US
# payload {
#  Query String Parameters {
#    tx: StateProperties=eyJUSUQiOiIzMzlkN2E0YS02MmNlLTQwNGEtYTU2My01YjI5ODdkZDMzZGYifQ
#    p: B2C_1A_SignInSignUp_en-US
#  }
#  Form Data {
#    request_type: RESPONSE
#    signInName: USERNAME
#    password: PASSWORD
#  }
#}
# RESPONSE HEADERS
# Location:

            _LOGGER.info('Succesfully fetched token')
            result = r.json()
            self.token = result['access_token']
            self.expiresAt = time.time() + result['expires_in']
            return True
        else:
            r.raise_for_status()

    def generate_url(self):
        region = self.region
        code1 = ''.join(random.choice(string.ascii_lowercase) for i in range(43))
        code_verifier = self.generate_hash(code1)
        self.login_input["code_verifier"] = code1
        url = f"""{REGIONS[region]["locale_url"]}/4566605f-43a7-400a-946e-89cc9fdb0bd7/B2C_1A_SignInSignUp_{REGIONS[region]["locale"]}/oauth2/v2.0/authorize?redirect_uri=fordapp://userauthorized&response_type=code&max_age=3600&code_challenge={code_verifier}&code_challenge_method=S256&scope=%2009852200-05fd-41f6-8c21-d36d3497dc64%20openid&client_id=09852200-05fd-41f6-8c21-d36d3497dc64&ui_locales={REGIONS[region]["locale"]}&language_code={REGIONS[region]["locale"]}&country_code={REGIONS[region]["locale_short"]}&ford_application_id={REGIONS[region]["region"]}"""
        _LOGGER.debug(f"generate_url:: {url}")
        return url

    def base64_url_encode(self, data):
        """Encode string to base64"""
        _LOGGER.debug(f"base64_url_encode:: {urlsafe_b64encode(data).rstrip(b'=')}")
        return urlsafe_b64encode(data).rstrip(b'=')

    def generate_hash(self, code):
        """Generate hash for login"""
        hashengine = hashlib.sha256()
        hashengine.update(code.encode('utf-8'))
        _LOGGER.debug(f"generate_hash:: {urlsafe_b64encode(hashengine.digest()).rstrip(b'=').decode('utf-8')}")
        return self.base64_url_encode(hashengine.digest()).decode('utf-8')

    def __acquireToken(self):
        '''Fetch and refresh token as needed'''

        if (self.token == None) or (time.time() >= self.expiresAt):
            _LOGGER.info('No token, or has expired, requesting new token')
            self.auth()
        else:
            _LOGGER.info('Token is valid, continuing')
            pass
    
    def status(self):
        '''Get the status of the vehicle'''

        self.__acquireToken() 

        params = {
            'lrdt': '01-01-1970 00:00:00'
        }

        headers = {
            **apiHeaders,
            'auth-token': self.token
        }

        r = requests.get(f'{baseUrl}/vehicles/v4/{self.vin}/status', params=params, headers=headers)
        
        if r.status_code == 200:
            result = r.json()
            return result['vehiclestatus']
        else:
            r.raise_for_status()
    
    def start(self):
        '''
        Issue a start command to the engine
        '''
        return self.__requestAndPoll('PUT', f'{baseUrl}/vehicles/v2/{self.vin}/engine/start')

    def stop(self):
        '''
        Issue a stop command to the engine
        '''
        return self.__requestAndPoll('DELETE', f'{baseUrl}/vehicles/v2/{self.vin}/engine/start')


    def lock(self):
        '''
        Issue a lock command to the doors
        '''
        return self.__requestAndPoll('PUT', f'{baseUrl}/vehicles/v2/{self.vin}/doors/lock')


    def unlock(self):
        '''
        Issue an unlock command to the doors
        '''
        return self.__requestAndPoll('DELETE', f'{baseUrl}/vehicles/v2/{self.vin}/doors/lock')

    def __makeRequest(self, method, url, data, params):
        '''
        Make a request to the given URL, passing data/params as needed
        '''

        headers = {
            **apiHeaders,
            'auth-token': self.token
        }        
    
        return getattr(requests, method.lower())(url, headers=headers, data=data, params=params)

    def __pollStatus(self, url, id):
        '''
        Poll the given URL with the given command ID until the command is completed
        '''
        status = self.__makeRequest('GET', f'{url}/{id}', None, None)
        result = status.json()
        if result['status'] == 552:
            _LOGGER.info('Command is pending')
            time.sleep(5)
            return self.__pollStatus(url, id) # retry after 5s
        elif result['status'] == 200:
            _LOGGER.info('Command completed succesfully')
            return True
        else:
            _LOGGER.info('Command failed')
            return False

    def __requestAndPoll(self, method, url):
        self.__acquireToken()
        command = self.__makeRequest(method, url, None, None)

        if command.status_code == 200:
            result = command.json()
            return self.__pollStatus(url, result['commandId'])
        else:
            command.raise_for_status()

    def __region_details(self):
        ''' get region details to build url '''
        if self.region in REGION_OPTIONS:
            region_details = REGIONS.get(self.region)
            return(region_details)
        else:
            _LOGGER.error("region:{region} not in REGION_OPTIONS:{REGION_OPTIONS}")
            return None

