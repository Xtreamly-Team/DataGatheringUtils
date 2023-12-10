from pprint import pprint
from eth_typing import HexStr
from web3 import Web3
import asyncio
import json
import time

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
from web3._utils.filters import Filter
from web3.types import LogReceipt



wss = 'wss://sly-attentive-lambo.quiknode.pro/701a96b9a9b95a0ad8bac7c49dc9ccbec618108e/'
web3 = Web3(Web3.WebsocketProvider(wss))
tx_filter = web3.eth.filter('pending')


# test to see if you are connected to your node
# this will print out True if you are successfully connected to a node
if web3.is_connected():
    print("Connected")

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

    except Exception as err:
        pass


async def log_loop():
    tx_filter = web3.eth.filter('pending')
    while True:
        try:
            for event in tx_filter.get_new_entries():
                handle_event(event)
        except Exception as e:
            print(time.time())
            await log_loop();

def main():
    # filter for pending transactions
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(log_loop())
    finally:
        loop.close()


if __name__ == '__main__':
    main()



