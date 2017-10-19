# send-OP_RETURN.py
# 
# CLI wrapper for OP_RETURN.py to send bitcoin with OP_RETURN metadata
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


def send(argv):
    if len(argv) < 4:
        sys.exit(
            '''Usage:
    python send_OP_RETURN.py send_address, send_amount, metadata, satoshis_per_byte=0 (optional), testnet=False (optional), repeats=0 
    
    Examples:
    python send_OP_RETURN.py 149wHUMa41Xm2jnZtqgRx94uGbZD9kPXnS 0.001 'Hello, blockchain!'
    python send_OP_RETURN.py 149wHUMa41Xm2jnZtqgRx94uGbZD9kPXnS 0.001 48656c6c6f2c20626c6f636b636861696e21
    python send_OP_RETURN.py mzEJxCrdva57shpv62udriBBgMECmaPce4 0.001 'Hello, testnet blockchain!' 20 1 0'''
        )

    dummy, send_address, send_amount, metadata = argv[0:4]
    satoshis_per_byte = 0
    if len(argv) > 4:
        satoshis_per_byte = argv[4]


    testnet = False
    if len(argv) > 5:
        testnet = bool(argv[5])

    repeats = 0
    if len(argv) > 6:
        repeats = argv[6]

    metadata_from_hex = OP_RETURN_hex_to_bin(metadata)
    if metadata_from_hex is not None:
        metadata = metadata_from_hex

    result = OP_RETURN_send(send_address, float(send_amount), metadata, float(satoshis_per_byte), testnet, repeats)

    if 'error' in result:
        print('Error: ' + result['error'])
    else:
        print('TxID: ' + result['txid'] + '\nWait a few seconds then check on: http://' +
              ('testnet.' if testnet else '') + 'coinsecrets.org/')

    return result

if __name__ == '__main__':
    send(sys.argv)