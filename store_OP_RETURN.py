# store-OP_RETURN.py
# 
# CLI wrapper for OP_RETURN.py to store data using OP_RETURNs
#
# Copyright (c) Coin Sciences Ltd
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import sys, string
from OP_RETURN import *


def store(argv):
    if len(argv) < 4:
        sys.exit(
            '''Usage:
            
    python store_OP_RETURN.py <send_address> <send_amount> <data> <satoshis_per_byte (optional)> <testnet (optional)> '''
        )


    send_address = argv[0]
    send_amount = argv[1]
    data = argv[2]
    satoshis_per_byte = 0

    if len(argv) > 4:
        satoshis_per_byte = float(argv[4])


    if len(argv) > 5:
        testnet = bool(argv[5])
    else:
        testnet = False

    data_from_hex = OP_RETURN_hex_to_bin(data)
    if data_from_hex is not None:
        data = data_from_hex

    result = OP_RETURN_store(send_address, send_amount, data, satoshis_per_byte, testnet)

    if 'error' in result:
        print('Error: ' + result['error'])
    else:
        print("TxIDs:\n" + "\n".join(result['txids']) + "\n\nRef: " + result[
            'ref'] + "\n\nWait a few seconds then check on: http://" +
              ('testnet.' if testnet else '') + 'coinsecrets.org/')


    return result
if __name__ == '__main__':
    store(sys.argv)