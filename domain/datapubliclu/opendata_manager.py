
from domain.datapubliclu import opendata_fetcher
from common import file_utils

import time
import os
import json

class OpenDataManager():

    def fetch_dataset(self, size):
        opendata_fetcher.get_dataset(size)

    def download_everything_in_the_world(self, filename):
        print('😱😱😱 DOWNLOADING ALLLLL THE DATA 😱😱😱')
        print('5sec to cancel...')
        time.sleep(5)

        data = file_utils.read_json(filename)

        destination = 'data/datasets/'

        supported_files = ['zip','csv', 'xml', 'geojson', 'json']

        i = 0
        size = 0

        null_filesize = []

        for d in data['data']:

            slug = 'unknown'
            name = 'unknown'

            if d['organization']:
                if d['organization']['slug']:
                    slug = d['organization']['slug']
                if d['organization']['name']:
                    name = d['organization']['name']

            destination_path = os.path.join(destination, slug)

            os.makedirs(destination_path, exist_ok=True) # Note: Even directories with no supported file are created

            resource_counter = 1
            for r in d['resources']:
                if r['format'] in supported_files:

                    if isinstance(r['filesize'],int):

                        i += 1
                        size += r['filesize']
                        print('File #',i)
                        #print(resource_counter, slug, r['format'], r['url'])

                        prefix = '{}_{}_'.format(resource_counter, slug)
                        if slug == 'unknown':
                            prefix += time.strftime("%Y%m%d-%H%M_")
                            
                        opendata_fetcher.download(r['url'], prefix, destination_path)

                        resource_counter += 1

                    else:
                        null_filesize.append(r)

        print('> TOTAL: {} files, {} GB'.format(i, size / (1000*1000*1000)))
        
        #for r in null_filesize:
        #    print(r['url'])



    # PRINT / STREAM
    ###################################################

    def print_dataset_info(self, filename):
        data = file_utils.read_json(filename)

        unique_formats = set()
        unique_mime = set()

        for d in data['data']:
            print('📔 DATASET: ID={}'.format(d['id']))
            print('   Title     : {}'.format(d['title']))
            print('   Resources : {}'.format(len(d['resources'])))

            for r in d['resources']:
                file_format = r['format']
                file_mime   = r['mime']
                
                unique_formats.add(file_format)
                unique_mime.add(file_mime)

                print('   💎 Resource ID={}'.format(r['id']))
                print('      Title  : {}'.format(r['title']))
                print('      Format : {}'.format(file_format))
                print('      Mime   : {}'.format(file_mime))

        print('*' * 20)
        print('Summary')
        print('  Formats:')
        for f in unique_formats:
            print(f)
        print('  Mimes:')
        for m in unique_mime:
            print(m)
            
    def print_datasets_as_json(self, filename):
        data = file_utils.read_json(filename)

        for d in data['data']:
            print( json.dumps(d) )


    def print_resources_as_json(self, filename):
        data = file_utils.read_json(filename)

        for d in data['data']:

            data_keys = ['id', 'license', 'frequency', 'tags', 'description', 'title', 'metrics', 'organization', 'uri', 'page', 'slug']

            data_for_resource = { 'data.{}'.format(key) : d[key] for key in data_keys }
            
            for r in d['resources']:
                r.update(data_for_resource)
                print( json.dumps(r) )

# DATA
#dict_keys(['resources', 'badges', 'frequency_date', 'owner', 'license', 'temporal_coverage', 
# 'last_update', 'spatial', 'extras', 'page', 'private', 'created_at', 'slug', 
# 'last_modified', 'metrics', 'deleted', 'tags', 'description', 'id', 
# 'uri', 'organization', 'title', 'frequency'])

# DATA > RESOURCE
# dict_keys(['filetype', 'checksum', 'url', 'format', 'last_modified', 'metrics', 'extras', 'mime', 
# 'id', 'published', 'description', 'title', 'created_at', 'latest', 'filesize'])