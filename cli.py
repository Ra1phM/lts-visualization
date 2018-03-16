import argparse
import logging

from domain.runner import Runner

# ARGUMENT PARSER
###################################################

parser = argparse.ArgumentParser(description='CLI for OpenData Portal')

parser.add_argument('--silent', 
                    action='store_true',
                    default=False,
                    help='Flag to only output the data and nothing else. Important for piping to logstash')

parser.add_argument('--save', 
                    action='store_true',
                    default=False,
                    help='Flag to save fetched files on disk. Good for safe backup. Careful! can overwrite existing ones!')

parser.add_argument('--endless', 
                    type=int,
                    help='Flag to forever query real-time APIs with a delay. Usage: --endless <seconds>')

# data.public.lu
###################################################

parser.add_argument('--fetch-dataset', 
                    type=int,
                    help='Fetch a certain amount of dataset information. (data.public.lu dataset API)')

parser.add_argument('--download-all', 
                    type=str,
                    help='Download everything in the world!!! (data.public.lu)')

parser.add_argument('--print-dataset', 
                    type=str,
                    help='Print the dataset file content. (data.public.lu dataset API)')

parser.add_argument('--stream-dataset-json', 
                    type=str,
                    help='Print each dataset as json.')

parser.add_argument('--stream-resources-json', 
                    type=str,
                    help='Print each resource as json.')

# Bike Data
###################################################

parser.add_argument('--bike-get-contracts',
                    action='store_true',
                    default=False,
                    help='Get all contracts or specific. (jcdecaux bike API)')

parser.add_argument('--bike-get-stations',
                    action='store_true',
                    default=False,
                    help='Get all stations. (jcdecaux bike API)')

parser.add_argument('--bike-get-stations-for-contract',
                    type=str,
                    help='Get all stations for a specific contract. (jcdecaux bike API)')

parser.add_argument('--bike-stream-contracts',
                    action='store_true',
                    default=False,
                    help='Stream all contracts or specific. (jcdecaux bike API)')

parser.add_argument('--bike-stream-stations',
                    action='store_true',
                    default=False,
                    help='Stream all stations. (jcdecaux bike API)')

parser.add_argument('--bike-stream-stations-for-contract',
                    type=str,
                    help='Stream all stations for a specific contract. (jcdecaux bike API)')

# Bus Data
###################################################

parser.add_argument('--bus-get-departures',
                    type=str,
                    help='Get departures of all. (Bus API)')

parser.add_argument('--bus-stream-departures',
                    type=str,
                    help='Stream departures of all. (Bus API)')

# General Streaming
###################################################

parser.add_argument('--stream-array-json',
                    type=str,
                    help='Print each json object in a json array.')

# LOGGER
###################################################

def setup_logging():
    # create logger
    logger = logging.getLogger() # The default logging
    logger.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s : [%(levelname)s] %(message)s')

    # Create File Logger
    fl = logging.FileHandler('logs/python-app.log', encoding="utf-8")
    fl.setFormatter(formatter)
    fl.propagate = True

    # Add loggers
    logger.addHandler(fl)

    logger.info('Logging initialized with great success!')

# MAIN
###################################################

if __name__ == '__main__':

    setup_logging()

    arguments = vars(parser.parse_args())

    runner = Runner()
    runner.run(arguments)
