from domain.bike import bike_api

from common import file_utils, time_utils

import logging
import json
import time

class BikeManager():

    def __init__(self):
        self.api = bike_api.BikeApi()

    def get_all_contracts(self, save=False):
        data = self.api.get_contracts()
        if save:
            file_utils.save_json(data, 'data/bike/bike_contracts.json')

        return data

    def get_all_stations(self, save=False):
        data = self.api.get_stations()
        if save:
            file_utils.save_json(data, 'data/bike/bike_stations-{}.json'.format(time_utils.get_time_str()))
        
        return data

    def get_stations_for_contract(self, contract='Luxembourg', save=False):
        data = self.api.get_stations_for_contract(contract)
        if save:
            file_utils.save_json(data, 'data/bike/bike_stations-{}-{}.json'.format(contract, time_utils.get_time_str()))

        return data


    def print_all_contracts(self, save=False):
        data = self.get_all_contracts(save)
        self.__print(data)

    def print_all_stations(self, save=False):
        data = self.get_all_stations(save)
        self.__print(data)

    def print_stations_for_contract(self, contract='Luxembourg', save=False):
        data = self.get_stations_for_contract(contract, save)
        self.__print(data)

    # STREAM all elements of json array individually (for logstash :))

    def stream_all_contracts(self, endless=None, save=False):
        self.__stream_all_contracts(save)

        if isinstance(endless, int):
            endless = abs(endless) # Only positive numbers
            logging.warn('Starting Endless Mode on Bike Contracts API. Endless={}'.format(endless))
            while True:
                time.sleep(endless)
                self.__stream_all_contracts(save)


    def stream_all_stations(self, endless=None, save=False):
        self.__stream_all_stations(save)

        if isinstance(endless, int):
            endless = abs(endless) # Only positive numbers
            logging.warn('Starting Endless Mode on Bike Stations API. Endless={}'.format(endless))
            while True:
                time.sleep(endless)
                self.__stream_all_stations(save)


    def stream_stations_for_contract(self, contract='Luxembourg', endless=None, save=False):
        self.__stream_stations_for_contract(contract, save)

        if isinstance(endless, int):
            endless = abs(endless) # Only positive numbers
            logging.warn('Starting Endless Mode on Bike Stations API. Endless={}'.format(endless))
            while True:
                time.sleep(endless)
                self.__stream_stations_for_contract(contract, save)

    # PRIVATE METHODS

    def __stream_all_contracts(self, save=False):
        data = self.get_all_contracts(save)
        self.__stream_array(data)

    def __stream_all_stations(self, save=False):
        data = self.get_all_stations(save)
        self.__stream_array(data)

    def __stream_stations_for_contract(self, contract='Luxembourg', save=False):
        data = self.get_stations_for_contract(contract, save)
        self.__stream_array(data)

    def __print(self, data):
        print( json.dumps( data ) )

    def __stream_array(self, data):
        for d in data:

            # FIX last_update because it has 13 things
            if 'last_update' in d:
                d['last_update'] = d['last_update']/1000

            self.__print(d)

    