from domain.app_config import get_config

import requests

class BusApi():

    def __init__(self):
        config = get_config()
        self.url = config['bus.api']['url']

    def get_departs_for_id(self, depart_id):
        ''' Returns JSON: [contract_json,contract_json,...]
        '''
        return self.__get(depart_id)


    def __get(self, depart_id):
        call = '{}?accessId=cdt&format=json&{}'.format(self.url, depart_id)

        return requests.get( call ).json()