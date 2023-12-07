from pprint import pprint
from eth_typing import HexStr
from web3 import Web3
import asyncio
import json
import time

from web3._utils.filters import Filter
from web3.types import LogReceipt



# enter your web socket node credentials here
# this will allow us to stream transactions
wss = 'wss://frosty-young-crater.ethereum-sepolia.quiknode.pro/d59c2507c5f6767d083cc7315dfa5e58325f4e98/'
web3 = Web3(Web3.WebsocketProvider(wss))

from eth_utils import (
    to_hex,
    is_list_like,
)

from hexbytes import (
    HexBytes,
)

from web3.datastructures import (
    AttributeDict,
)

from typing import (
    Dict, Any, Union, Iterable, Optional, Type
)

# test to see if you are connected to your node
# this will print out True if you are successfully connected to a node
if web3.is_connected():
    print("Connected")

# ('{"blockHash": null, "blockNumber": null, "from": '
#  '"0x2c6671BdF3749eE6d33741e3C3c2D6A23D2b9B3e", "gas": 2100000, "gasPrice": '
#  '207555201, "maxFeePerGas": 207555201, "maxPriorityFeePerGas": 11, "hash": '
#  '"0x0cddbb0b0f22a4452efffcf3cf4e9736859a2489760f6ea9ee96d75708701dc8", '
#  '"input": '
#  '"0xef16e8450000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000000000000000c0c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470000000000000000000000000100077770000000000000000000000000000000100000000000000000000000000000000000000000000000000000000004c4b400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000", '
#  '"nonce": 1503214, "to": "0x6375394335f34848b850114b66A49D6F47f2cdA8", '
#  '"transactionIndex": null, "value": 0, "type": 2, "accessList": [], '
#  '"chainId": 11155111, "v": 0, "r": '
#  '"0x127e820e89528e2b4969679d5d3aafd9196ce0451129424b1d1d499ed21c4097", "s": '
#  '"0x2a68363386f598dbc94c5737842770ccc1de595c8dca356104b546afcbe64c41", '
#  '"yParity": 0, "timestamp": 1000}')

def handle_event(event: HexStr):
    # use a try / except to have the program continue if there is a bad transaction in the list
    try:
        transaction = web3.eth.get_transaction(event)
        result = {}
        result['hash'] = transaction['hash'].hex()
        result['from'] = transaction['from']
        result['to'] = transaction['to']
        result['input'] = transaction['input'].hex()
        result['gas'] = transaction['gas']
        result['gasPrice'] = transaction['gasPrice']
        result['maxFeePerGas'] = transaction['maxFeePerGas']
        result['maxPriorityFeePerGas'] = transaction['maxPriorityFeePerGas']
        result['nonce'] = transaction['nonce']
        result['chainId'] = transaction['chainId']
        result['timestamp'] = time.time()
        print(json.dumps(result));
        print("", flush=True)
        # my_dict = dict(transaction.items())
        # my_dict['timestamp'] = 1000
        # pprint(to_json(my_dict))

    except Exception as err:
        # print transactions with errors. Expect to see transactions people submitted with errors 
        # print(f'error: {err}')
        pass


async def log_loop(event_filter: Filter, poll_interval: float):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        await asyncio.sleep(poll_interval)


def main():
    # filter for pending transactions
    tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(tx_filter, 2)))
    finally:
        loop.close()


if __name__ == '__main__':
    main()



