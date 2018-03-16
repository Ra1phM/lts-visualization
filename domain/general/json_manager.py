from common import file_utils
import json

class JsonManager():

    @staticmethod
    def print_array(filename):
        ''' Read the file and print each element from a JSON array: [d1, d2, d3,....]
        '''
        data = file_utils.read_json(filename)

        for d in data:
            print( json.dumps(d) )
        