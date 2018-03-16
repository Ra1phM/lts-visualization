import requests
import os

from common import file_utils

API = 'https://data.public.lu/api/1/'

def get_dataset(page_size=20):
    url = API + 'datasets/?page_size={}'.format(page_size)
    
    print('⏰ Calling {}...'.format(url))
    data = requests.get(url)

    filename = 'data/datasets.json'
    
    print('Done.')

    print('⏰ Saving to {}...'.format(filename))

    file_utils.save_json(data.json(), filename)

    print('Done.')

def download(url, prefix, destination):
    local_filename = prefix + url.split('/')[-1]

    output = os.path.join(destination, local_filename)
    
    print('⏰ Downloading')
    print('    FROM : {}'.format(url))
    print('    TO   : {}'.format(output))
    
    try:
        r = requests.get(url, stream=True)

        with open(output, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)
    except:
        print('ERROR downloading.')

    print('Done.')



    