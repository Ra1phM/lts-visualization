import logging
import json
import os
import time

from common import file_utils
from domain.datapubliclu import opendata_manager

from domain.general import json_manager
from domain.bike import bike_manager
from domain.bus import bus_manager


class Runner():

    is_silent = False

    save = False

    def cliprint(self, message):
        logging.info(message)
        if not self.is_silent:
            print(message)

    def run(self, arguments):
        ''' Starting point of the command line tool.
        '''
        self.is_silent  = arguments['silent']
        self.save       = arguments['save']
        self.endless    = arguments['endless']

        self.cliprint('🛠 🛠  START CLI 🛠 🛠')

        fetch_dataset           = arguments['fetch_dataset']
        download_all            = arguments['download_all']
        print_dataset           = arguments['print_dataset']
        stream_dataset_json     = arguments['stream_dataset_json']
        stream_resources_json   = arguments['stream_resources_json']

        bike_get_contracts                  = arguments['bike_get_contracts']
        bike_get_stations                   = arguments['bike_get_stations']
        bike_get_stations_for_contract      = arguments['bike_get_stations_for_contract']

        bike_stream_contracts               = arguments['bike_stream_contracts']
        bike_stream_stations                = arguments['bike_stream_stations']
        bike_stream_stations_for_contract   = arguments['bike_stream_stations_for_contract']

        bus_get_departures       = arguments['bus_get_departures']
        bus_stream_departures    = arguments['bus_stream_departures']

        stream_array_json       = arguments['stream_array_json']

        if fetch_dataset and isinstance(fetch_dataset, int):
            self.cliprint('Command: Fetch Dataset')
            m = opendata_manager.OpenDataManager()
            m.fetch_dataset(fetch_dataset)
            return

        if download_all:
            self.cliprint('Command: DOWNLOAD EVERYTHING')
            m = opendata_manager.OpenDataManager()
            m.download_everything_in_the_world(download_all)
            return

        if print_dataset:
            self.cliprint('Command: Print Dataset')
            m = opendata_manager.OpenDataManager()
            m.print_dataset_info(print_dataset)
            return

        if stream_dataset_json:
            self.cliprint('Command: Print Datasets as JSON')
            m = opendata_manager.OpenDataManager()
            m.print_datasets_as_json(stream_dataset_json)
            return

        if stream_resources_json:
            self.cliprint('Command: Print Resources as JSON')
            m = opendata_manager.OpenDataManager()
            m.print_resources_as_json(stream_resources_json)
            return

        # BIKE - GET
        
        if bike_get_contracts:
            self.cliprint('Command: Print Bike Contracts as JSON')
            bm = bike_manager.BikeManager()
            bm.print_all_contracts(self.save)
            return

        if bike_get_stations:
            self.cliprint('Command: Print Bike Stations as JSON')
            bm = bike_manager.BikeManager()
            bm.print_all_stations(self.save)
            return

        if bike_get_stations_for_contract:
            self.cliprint('Command: Print Bike Stations as JSON')
            bm = bike_manager.BikeManager()
            bm.print_stations_for_contract(bike_get_stations_for_contract, self.save)
            return

        # BIKE - STREAM

        if bike_stream_contracts:
            self.cliprint('Command: Stream Bike Contracts as JSON')
            bm = bike_manager.BikeManager()
            bm.stream_all_contracts(self.endless, self.save)
            return

        if bike_stream_stations:
            self.cliprint('Command: Stream Bike Stations as JSON')
            bm = bike_manager.BikeManager()
            bm.stream_all_stations(self.endless, self.save)
            return

        if bike_stream_stations_for_contract:
            self.cliprint('Command: Stream Bike Stations as JSON')
            bm = bike_manager.BikeManager()
            bm.stream_stations_for_contract(bike_stream_stations_for_contract, self.endless, self.save)
            return

        # BUS

        if bus_get_departures:
            self.cliprint('Command: Stream Bus Departues as JSON')
            bm = bus_manager.BusManager()
            bm.print_all_departues(bus_get_departures, self.save)
            return

        if bus_stream_departures:
            self.cliprint('Command: Stream Bus Departues as JSON')
            bm = bus_manager.BusManager()
            bm.stream_all_departues(bus_stream_departures, self.endless, self.save)
            return

        # General JSON

        if stream_array_json:
            self.cliprint('Command: Print each JSON Element from JSON array.')
            json_manager.JsonManager.print_array(stream_array_json)

