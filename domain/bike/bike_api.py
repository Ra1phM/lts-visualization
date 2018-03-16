from domain.app_config import get_config

import requests

class BikeApi():

    def __init__(self):
        config = get_config()
        self.url = config['bike.api']['url']
        self.api_key = config['bike.api']['apiKey']

    def get_contracts(self):
        ''' Returns JSON: [contract_json,contract_json,...]
        '''
        return self.__get('contracts')

    def get_stations(self):
        ''' Returns JSON: [station_json, station_json, ...]
        '''
        return self.__get('stations')

    def get_stations_for_contract(self, contract):
        ''' Get stations for a specific contract.
        Returns JSON: [station_json, station_json, ...]
        '''
        return self.__get('stations', '&contract={}'.format(contract))

    def __get(self, endpoint, parameters=''):
        call = '{}{}?apiKey={}{}'.format(self.url, endpoint, self.api_key, parameters)

        return requests.get( call ).json()