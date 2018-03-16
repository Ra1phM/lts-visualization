import argparse

import pandas as pd

# ARGUMENT PARSER
###################################################

parser = argparse.ArgumentParser(description='CLI for testing and checking CSV files')

parser.add_argument('--input',
                    type=str,
                    help='Get departures of all. (Bus API)')

parser.add_argument('--output',
                    type=str,
                    help='Stream departures of all. (Bus API)')

# CSV Checker
###################################################

def run(arguments):
    input_csv   = arguments['input']
    output_csv  = arguments['output']

    data = None
    
    # Try with comma
    data, success = read(input_csv, ',')

    # Try with semi-colon
    if not success:
        data,success = read(input_csv, ';')
    
    if success:
        print('👍 Not problem with this CSV.')

        if output_csv:
            data.to_csv(output_csv, index=False)
            print('CSV saved to: {}'.format(output_csv))

    else:
        print('👎 This csv is broken...')


def read(filename, delimiter):
    try:
        data = pd.read_csv(filename, delimiter=delimiter)
        print('Success loading {} using "{}"'.format(filename, delimiter))
        return data, True
    except:
        print('Fail loading {} using "{}"'.format(filename, delimiter))
        return None, False


# MAIN
###################################################

if __name__ == '__main__':

    arguments = vars(parser.parse_args())

    run(arguments)

    
