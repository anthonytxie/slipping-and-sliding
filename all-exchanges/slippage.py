import ccxt
import numpy as np
import pandas as pd
import time
import json
import threading

exchange_names = ['binance', 'bitmex', 'okex','zb','huobipro', 'bitforex', 'bitfinex','hitbtc2','bibox','lbank','gdax','kraken','bittrex','poloniex']
print(len(exchange_names))
def load_pairs():
    print('loading pairs')
    pairs = { }
    for index, exchange_name in enumerate(exchange_names):
        if exchange_name == 'bibox':
            pairs[exchange_name] = list(ccxt.bibox({'apiKey': '0d218d65c98fe7941bf5f51cc6fcec874fc9706d','secret': 'caa17d59c68c8f8c09987774d98f52428a3834bf'}).load_markets().keys())
        else:
            pairs[exchange_name] = list(getattr(ccxt, exchange_name)().load_markets().keys())
    return pairs

pairs = load_pairs()

def log_for(pairs, name, current_time):
    if name == 'bibox':
        exchange = ccxt.bibox({'apiKey': '0d218d65c98fe7941bf5f51cc6fcec874fc9706d','secret': 'caa17d59c68c8f8c09987774d98f52428a3834bf'})
    else:
        exchange = getattr(ccxt, name)()
    exchange_dict = {}
    for symbol in pairs:
        print('trying for', symbol)
        try:
            order_book = exchange.fetch_l2_order_book(symbol)
            exchange_dict[symbol] = {'asks':[], 'bids':[]}
            exchange_dict[symbol]['asks'] = order_book['asks']
            exchange_dict[symbol]['bids'] = order_book['bids']
        except:
            print('no luck for', symbol)
    with open(str(current_time)+ '_' + name + '_orderbook.json', "w") as outfile:
        print('writing to file')
        json.dump(exchange_dict, outfile, indent=4)

class MyThread(threading.Thread):
    def __init__(self, exchange_name, pairs, current_time):
        super().__init__()
        self.exchange_name = exchange_name
        self.pairs = pairs
        self.current_time = current_time

    def run(self):
        log_for(self.pairs, self.exchange_name, self.current_time)

while True:
    current_time = int(time.time() * 1000)
    threads = list()
    for i, ex in enumerate(exchange_names):
        threads.append(MyThread(ex, pairs[ex], current_time))
        threads[i].start()

    for t in threads:
        t.join()

    time.sleep(60*60)
