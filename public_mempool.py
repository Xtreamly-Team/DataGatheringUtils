from pprint import pprint
from eth_typing import HexStr
from web3 import Web3
import asyncio
import json

from web3._utils.filters import Filter
from web3.types import LogReceipt

# enter your web socket node credentials here
# this will allow us to stream transactions
wss = 'wss://frosty-young-crater.ethereum-sepolia.quiknode.pro/d59c2507c5f6767d083cc7315dfa5e58325f4e98/'
web3 = Web3(Web3.WebsocketProvider(wss))


# test to see if you are connected to your node
# this will print out True if you are successfully connected to a node
print(web3.is_connected())


def handle_event(event: HexStr):
    print(type(event))
    print("EVENT")
    # print the transaction hash
    # print(Web3.toJSON(event))

    # use a try / except to have the program continue if there is a bad transaction in the list
    try:
        # remove the quotes in the transaction hash
        # transaction = Web3.to_json(event).strip('"')
        # event.
        # use the transaction hash that we removed the '"' from to get the details of the transaction
        transaction = web3.eth.get_transaction(event)
        # print the transaction and its details
        pprint(transaction)

    except Exception as err:
        # print transactions with errors. Expect to see transactions people submitted with errors 
        print(f'error: {err}')


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
