from pprint import pprint
from asyncio import run
from ccxt.pro import binance, kucoin, coinbase, bitget, bitmex

binance = binance({'apiKey': '', 'secret': ''})
kucoin = kucoin({'apiKey': '', 'secret': ''})
bitget = bitget({'apiKey': '', 'secret': ''})
bitmex = bitmex({'apiKey': '', 'secret': ''})

async def main():
    while True:
        orderbook1 = await binance.watch_order_book('BTC/USDT')
        orderbook2 = await kucoin.watch_order_book('BTC/USDT')
        orderbook4 = await bitget.watch_order_book('BTC/USDT')
        orderbook5 = await bitmex.watch_order_book('BTC/USDT')
        pprint({
            'binance': orderbook1['bids'][0],
            'kucoin': orderbook2['bids'][0],
            # 'coinbase': orderbook3['bids'][0],
            'bitget': orderbook4['bids'][0],
            'bitmex': orderbook5['bids'][0],
        })
        # print(orderbook['asks'][0], orderbook['bids'][0])
    await binance.close()
    await kucoin.close()
    await coinbase.close()
    await bitget.close()
    await bitmex.close()

run(main())
