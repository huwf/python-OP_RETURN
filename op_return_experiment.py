import os
import json
import requests
import sys
from datetime import datetime
from send_OP_RETURN import send
from store_OP_RETURN import store
import logging

log = logging.getLogger('__main__')

TESTNET = 1
ADDRESS = ''
if len(sys.argv) < 2:
    print('You must at least include a wallet address!')
    sys.exit(1)
else:
    ADDRESS = sys.argv[1]

output_path = os.path.join(os.getcwd(), 'stored_data')


def get_data():
    with open('%s/%s.json' % (output_path, datetime.strftime(datetime.now(), '%Y%m%d%H%M%S')), 'w') as f:
        js = requests.get('https://bitcoinfees.21.co/api/v1/fees/list').json()
        json.dump(js, f)


def run_code():
    with open(os.path.join(os.getcwd(), 'input_data.txt')) as f:
        for i in range(0, 290, 10):
            i = 200
            send(['send', ADDRESS, 0, f.read(), i, TESTNET])
            log.info('Completed "send" function')
            # store(['store', f.read(), ADDRESS, i, TESTNET])
            break

if __name__ == '__main__':
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    get_data()
    run_code()

