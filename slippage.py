import ccxt
import numpy as np
import pandas as pd
import time
import json

bitmex = ccxt.bitmex()
bithumb = ccxt.bithumb()
okex = ccxt.okex()
binance = ccxt.binance()
huobi = huobi = ccxt.huobipro()
bitforex = ccxt.bitforex()
bittrex = ccxt.bittrex()
kraken = ccxt.kraken()
gdax = ccxt.gdax()
bitfinex = ccxt.bitfinex2()

exchange_names = ['bithumb']
exchanges = [bithumb]


bithumb.load_markets()


def load_pairs():
    pairs = { }
    for index, exchange in enumerate(exchange_names):
        pairs[exchange] = list(exchanges[index].load_markets().keys())
    return pairs

pairs = load_pairs()

def orderbook_to_textfile(exchanges, exchange_names, pairs):
    current_time = int(time.time() * 1000)
    exchanges_list = []
    for index,exchange in enumerate(exchanges):
        print(exchange_names[index])
        exchange_dict = {'exchange_name': exchange_names[index]}
        for symbol in pairs[exchange_names[index]]:
            print('trying for', symbol)
            try:
                order_book = exchange.fetch_l2_order_book(symbol)
                exchange_dict[symbol] = {'asks':[], 'bids':[]}
                exchange_dict[symbol]['asks'] = order_book['asks']
                exchange_dict[symbol]['bids'] = order_book['bids']
            except:
                print('no luck for', symbol)
        exchanges_list.append(exchange_dict)
    with open(str(current_time)+'_orderbook.json', "w") as outfile:
        print('writing to file')
        json.dump(exchanges_list, outfile, indent=4)
    return exchanges_list

while True:
    try:
        print('getting orderbooks')
        orderbook_to_textfile(exchanges, exchange_names, pairs)
    except:
        print('pass')
    time.sleep(60*60)
