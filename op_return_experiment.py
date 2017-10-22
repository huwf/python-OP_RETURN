import os
import json
import requests
import sys
from datetime import datetime
from send_OP_RETURN import send
from store_OP_RETURN import store
from OP_RETURN import SATOSHI_BTC_VALUE
import logging
import csv
import time
from collections import OrderedDict

log = logging.getLogger('__main__')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())
log.debug('Log set to level %s' % str(log.level))

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
        js = requests.get('https://bitcoinfees.21.co/api/v1/fees/list').text
        js_obj = json.loads(js, object_pairs_hook=OrderedDict)
        json.dump(js_obj, f)
        return js_obj



def do_transactions(func, testnet):
    with open(os.path.join(os.getcwd(), 'input_data.txt')) as f:
        func_str = func.__name__
        data = f.read()
        path = get_and_create_path(OUTPUT_PATH, datetime.now())
        with open('%s/%s.csv' % (path, func_str), 'w') as output:
            writer = csv.writer(output)
            headings = [func_str, 'txid', 'satoshis_per_byte', 'sent_stamp']
            if func_str == 'store':
                headings.append('ref')
            writer.writerow(headings)
            for i in range(290, 0, -40):
                # i = 20
                result = func([func_str, ADDRESS, 0, data, i, testnet])
                log.info('Completed "%s" function with fees of %d' % (func_str, i))
                if 'txids' in result:
                    for txid in result['txids']:
                        writer.writerow(
                            [func_str, txid, i, datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S'), result['ref']])

                else:
                    writer.writerow([func_str, result['txid'], i, datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')])
                # break
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
    return transaction


def calculate_price_points(amount_of_points):
    js = get_fees_data()
    index = 0
    zero_fee = 0
    zero_fee_gap = 0
    fees = js['fees']
    for key in fees:
        if key['maxDelay'] == 0:
            zero_fee = key['minFee']
            print('zero_fee = %d' % zero_fee)
            break
        index += 1

    total_fee = 0
    fees = []
    for i in range(zero_fee, 10, -(int(zero_fee/amount_of_points))):
        fee = i - (i%10) + 1
        print(fee)
        fees.append(fee)
    return fees


    # for k in range(index, 1, -(int(len(fees[0:index])/7))):
    #     print(fees[k])



def calculate_transaction_costs(path, price_points, testnet):
    with open(path) as f:
        reader = csv.reader(f)
        headers = next(reader, None)

        tx_id = next(reader, None)[1]
        transaction = get_transaction_info(tx_id, testnet)
        size = transaction['size']
        total_fee = 0

        for fee in price_points:
            # fee = transaction['total_fee']
            total_fee += (size * fee)

        return total_fee
        # break


def calculate_multiple_transaction_costs(path, price_points, testnet):
    with open(path) as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        size = 0
        total_fee = 0
        for i in range(3):
            tx_id = next(reader, None)[1]
            transaction = get_transaction_info(tx_id, testnet)
            size += transaction['size']

        for fee in price_points:
            # fee = transaction['total_fee']
            total_fee += (size * fee)

        return total_fee


if __name__ == '__main__':
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    testnet = False
    if len(sys.argv) > 2:
        testnet = sys.argv[2]
    log.info('Setting testnet to %s' % str(testnet))

    # get_fees_data()
    # get_latest_block(testnet)
    # do_transactions(send, testnet)
    # do_transactions(store, testnet)


    path = get_and_create_path(OUTPUT_PATH, datetime.now())
    points = calculate_price_points(6)
    # Setting points to a single transaction at the mean cost
    points = [86]
    total_cost = calculate_transaction_costs('%s/send.csv' % path, points, 1)
    total_cost_multiple = calculate_multiple_transaction_costs('%s/store.csv' % path, points, 1)
    print('total cost: %f + %f = %f' % (total_cost, total_cost_multiple, (total_cost + total_cost_multiple)))



