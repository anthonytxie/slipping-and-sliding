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

exchange_names = ['bithumb', 'bitmex','okex','binance', 'huobi', 'bitforex', 'bittrex', 'bitfinex', 'kraken', 'gdax']
exchanges = [bithumb, bitmex, okex, binance, huobi, bitforex, bittrex, bitfinex, kraken, gdax]


pairs = {
    'bithumb': ['ZEC/KRW','XMR/KRW','BTC/KRW','WTC/KRW','EOS/KRW','LTC/KRW','ETC/KRW','ETH/KRW','QTUM/KRW','BCH/KRW'],

    'bitmex': ['BTC/USD'],

    'okex': ['BCH/USDT','BTC/USDT','BCH/BTC','ETH/USDT','EOS/USDT','LTC/BTC','ETH/BTC','EOS/BTC','LTC/USDT','ETC/USDT'],

    'binance': ['BCH/BTC','BCH/USDT','BTC/USDT','ETH/BTC','ETH/USDT','XRP/BTC','XRP/USDT','ADA/BTC','EOS/USDT','PAX/BTC'],

    'huobi': ['BTC/USDT','BCH/USDT','ETH/USDT','EOS/USDT','BCH/BTC','EOS/BTC','EOS/ETH','XRP/USDT','ETH/BTC','LTC/USDT'],

    'bitforex': ['BTC/USDT','BCH/USDT','ETH/USDT','LTC/USDT','TRX/USDT','NEO/ETH','ETC/USDT','NEO/USDT','QTUM/ETH','QTUM/USDT'],

    'bittrex': ['BCH/BTC','BTC/USD','ADA/BTC','ETH/BTC','XRP/BTC','BCH/USDT','RVN/BTC','BTC/USDT','HYDRO/BTC','LTC/BTC'],

    'bitfinex': ['BCH/USD','BTC/USD','ETH/USD','USDT/USD','XRP/USD','BCH/BTC','EOS/USD','LTC/USD','ETH/BTC','DASH/USD','MIOTA/USD','NEO/USD','BTC/EUR','XRP/BTC','ETC/USD','BTG/USD','ETH/EUR','LTC/BTC','EOS/BTC','XMR/USD','ZEC/USD','DASH/BTC'],

    'kraken': ['ETH/USD','BTC/EUR','BTC/USD','ETH/EUR','BCH/EUR','BCH/USD','XRP/USD','BCH/BTC','XRP/EUR','ETH/BTC'],

    'gdax': ['BCH/USD','BTC/USD','ETH/USD','LTC/USD','BCH/BTC','BCH/EUR','BTC/EUR','ZRX/USD','LTC/BTC', 'ETC/USD'],
}



def orderbook_to_textfile(exchanges, exchange_names,pairs):
    current_time = int(time.time() * 1000)
    exchanges_list = []
    for index,exchange in enumerate(exchanges):
        exchange_dict = {'exchange_name': exchange_names[index]}
        for symbol in pairs[exchange_names[index]]:
            try:
                order_book = exchange.fetch_l2_order_book(symbol)
                exchange_dict[symbol] = {'asks':[], 'bids':[]}
                exchange_dict[symbol]['asks'] = order_book['asks']
                exchange_dict[symbol]['bids'] = order_book['bids']
            except:
                pass
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
