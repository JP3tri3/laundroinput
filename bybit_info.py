import bybit
import config
import json

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)

# info = client.Market.Market_symbolInfo().result()
# keys = info[0]['result']

# btcOrderBookInfo = client.Market.Market_orderbook(symbol="BTCUSD").result()

# inverse perpetual keys
# btcInfo = keys[0]
# ethInfo = keys[1]
# eosInfo = keys[2]
# xrpInfo = keys[3]

# # usdt perpetual keys
# btcusdtInfo = keys[4]
# ethusdtInfo = keys[5]
# ltcusdtInfo = keys[6]
# linkusdtInfo = keys[7]
# xtzusdtInfo = keys[8]

# # Price Information:
# ethLastPrice = ethInfo['last_price']


# eth Balance in USD
# myEthBalanceUSD = float(ethLastPrice) * myEthBalance

# Wallet Balances:


def btcWallet():
    myBtcWallet = client.Wallet.Wallet_getBalance(coin="BTC").result()
    myBtcBalance = myBtcWallet[0]['result']['BTC']['available_balance']
    print(myBtcBalance)


def ethWallet():
    myEthWallet = client.Wallet.Wallet_getBalance(coin="ETH").result()
    myEthBalance = myEthWallet[0]['result']['ETH']['available_balance']
    print(myEthBalance)

# BTC Info:


def btcPriceInfo():
    info = client.Market.Market_symbolInfo().result()
    keys = info[0]['result']
    btcInfo = keys[0]

    btcLastPrice = btcInfo['last_price']
    btcMarkPrice = btcInfo['mark_price']
    btcAskPrice = btcInfo['ask_price']
    btcIndexPrice = btcInfo['index_price']

    print("")
    print("Last Price: " + btcLastPrice)
    print("Mark Price: " + btcMarkPrice)
    print("Ask Price: " + btcAskPrice)
    print("Index Price: " + btcIndexPrice)
    print("")


def btcLastPrice():
    info = client.Market.Market_symbolInfo().result()
    keys = info[0]['result']
    btcInfo = keys[0]['last_price']
    return float(btcInfo)


def btcInfo():
    info = client.Market.Market_symbolInfo().result()
    keys = info[0]['result']
    btcInfo = keys[0]
    print(btcInfo)


# def btcActiveOrder():
#     activeOrder = client.LinearOrder.LinearOrder_getOrders(
#         symbol="BTCUSD").result()
#     activeOrderResult = activeOrder[0]['result']
#     return activeOrderResult

def activeOrder():
    activeOrder = client.Order.Order_query(symbol="BTCUSD").result()
    # print(activeOrder)
    order = activeOrder[0]['result']
    if (order == []):
        return 0
    else:
        return 1


def cancelAllOrders(symbol):
    client.Order.Order_cancelAll(symbol=symbol).result()


# def cancelOrder(symbol, orderId):
#     client.Order.Order_cancel(symbol=symbol, order_id=orderId).result()


def myPosition():
    position = client.Positions.Positions_myPosition(symbol="BTCUSD").result()
    print(position)


def changeStopLoss(symbol, subtract):
    stop_loss = str(btcLastPrice() - subtract)
    client.Positions.Positions_tradingStop(
        symbol=symbol, stop_loss=stop_loss).result()
