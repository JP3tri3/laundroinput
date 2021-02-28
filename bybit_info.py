import bybit
import config

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)

info = client.Market.Market_symbolInfo().result()
keys = info[0]['result']

btcOrderBookInfo = client.Market.Market_orderbook(symbol="BTCUSD").result()

# inverse perpetual keys
btcInfo = keys[0]
ethInfo = keys[1]
eosInfo = keys[2]
xrpInfo = keys[3]

# usdt perpetual keys
btcusdtInfo = keys[4]
ethusdtInfo = keys[5]
ltcusdtInfo = keys[6]
linkusdtInfo = keys[7]
xtzusdtInfo = keys[8]

# wallet balance:
myBtcWallet = client.Wallet.Wallet_getBalance(coin="BTC").result()
myEthWallet = client.Wallet.Wallet_getBalance(coin="ETH").result()

myBtcBalance = myBtcWallet[0]['result']['BTC']['available_balance']
myEthBalance = myEthWallet[0]['result']['ETH']['available_balance']

# Price Information:
ethLastPrice = ethInfo['last_price']
btcLastPrice = btcInfo['last_price']
btcMarkPrice = btcInfo['mark_price']
btcAskPrice = btcInfo['ask_price']
btcIndexPrice = btcInfo['index_price']

# eth Balance in USD
myEthBalanceUSD = float(ethLastPrice) * myEthBalance