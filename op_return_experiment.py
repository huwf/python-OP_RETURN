import os
import json
import requests
import sys
from datetime import datetime
from send_OP_RETURN import send
from store_OP_RETURN import store
import logging
import csv
import time

log = logging.getLogger('__main__')


def get_api_info():
    with open('api_keys.json') as f:
        return json.load(f)


API_INFO = get_api_info()
ADDRESS = ''
if len(sys.argv) < 2:
    print('You must at least include a recipient address!')
    sys.exit(1)
else:
    ADDRESS = sys.argv[1]

OUTPUT_PATH = os.path.join(os.getcwd(), 'stored_data', 'output')


def get_and_create_path(output_path, now):
    date_list = datetime.strftime(now, '%Y%m%d %H').split(' ')
    date = date_list[0]
    time = date_list[1]
    path = '%s/%s/%s' % (output_path, date, time)
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def get_fees_data():
    path = get_and_create_path(OUTPUT_PATH, datetime.now())
    with open('%s/fees.json' % path, 'w') as f:
        js = requests.get('https://bitcoinfees.21.co/api/v1/fees/list').json()
        json.dump(js, f)


def do_transactions(func, testnet):
    with open(os.path.join(os.getcwd(), 'input_data.txt')) as f:
        func_str = func.__name__
        path = get_and_create_path(OUTPUT_PATH, datetime.now())
        with open('%s/%s.csv' % (path, func_str), 'w') as output:
            writer = csv.writer(output)
            headings = [func_str, 'txid', 'satoshis_per_byte', 'sent_stamp']
            if func_str == 'store':
                headings.append('ref')
            writer.writerow(headings)
            for i in range(290, 0, -20):
                i = 20
                result = func([func_str, ADDRESS, 0, f.read(), i, testnet])
                log.info('Completed "%s" function with fees of %d' % (func_str, i))
                if 'txids' in result:
                    for txid in result['txids']:
                        writer.writerow(
                            [func_str, txid, i, datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S'), result['ref']])

                else:
                    writer.writerow([func_str, result['txid'], i, datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')])
                break
                # We don't want to end up with too many transactions in the mempool at any one time
                # This should hopefully reduce the amount
                time.sleep(5)


def get_latest_block(testnet):
    api_key = API_INFO['API_KEY']
    url = 'https://api.blocktrail.com/v1/%s/block/latest?api_key=%s' % ('tbtc' if testnet else 'btc', api_key)
    with open(os.path.join(get_and_create_path(OUTPUT_PATH, datetime.now()), 'latest_block.json'), 'w') as f:
        js = requests.get(url).json()
        json.dump(js, f)
        return js


def get_transaction_info(hash, testnet):
    api_key = API_INFO['API_KEY']
    url = 'https://api.blocktrail.com/v1/%s/transaction/%s?api_key=%s' % ('tbtc' if testnet else 'btc', hash, api_key)
    transaction = requests.get(url).json()
    print(transaction)


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    testnet = False
    if len(sys.argv) > 2:
        testnet = sys.argv[2]
    log.info('Setting testnet to %s' % str(testnet))

    get_fees_data()
    get_latest_block(testnet)
    do_transactions(send, testnet)
    do_transactions(store, testnet)



