from domain.bus import bus_api

from common import file_utils, time_utils

import logging
import json
import time

from multiprocessing import Process, Pool

def unwrap_self_get_departures(arg, **kwarg):
    return BusManager._get_departures(*arg, **kwarg)

class BusManager():

    def __init__(self):
        self.api = bus_api.BusApi()

    def _get_departures(self, query):
        ''' Return the list of 'Departure' elements.
        '''
        try:
            query = query.replace('\n', '').replace(';','')

            departures = self.api.get_departs_for_id(query)
            if 'Departure' in departures:
                # Add query to all departures
                for d in departures['Departure']:
                    d['original_query'] = query

                return departures['Departure']
        except Exception as e:
            logging.error('Failed to process: ' + query)

        return []

    def get_all_departues(self, filename, save=False):

        data = []

        pool = Pool(processes=10)

        with open(filename, 'r') as f:
            queries = f.readlines()

            results = pool.map(BusManager()._get_departures, queries)

            for r in results:
                data.extend(r)
        
            logging.info('{} Departures fetched from {} stations.'.format(len(data), len(queries)))

            if save:
                file_utils.save_json(data, 'data/bus/live/bus_departures-{}-{}.json'.format('1', time_utils.get_time_str()))

            return data

    def print_all_departues(self, filename, save=False):
        data = self.get_all_departues(filename, save)

    def stream_all_departues(self, filename, endless=None, save=False):
        self.__stream_all_departues(filename, save)

        if isinstance(endless, int):
            endless = abs(endless) # Only positive numbers
            logging.warn('Starting Endless Mode on Bus Departues API. Endless={}'.format(endless))
            while True:
                time.sleep(endless)
                self.__stream_all_departues(filename, save)

    def __stream_all_departues(self, filename, save=False):
        data = self.get_all_departues(filename, save)
        for d in data:
            self.__print(d)

    def __print(self, data):
        print( json.dumps( data ) )