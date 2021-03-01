import bybit
import config
import json
import time
import datetime

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)

orderId = ""
orderPrice = 0
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

def cancelAllOrders(symbol):
    client.Order.Order_cancelAll(symbol=symbol).result()


# def cancelOrder(symbol, orderId):
#     client.Order.Order_cancel(symbol=symbol, order_id=orderId).result()

def timeStamp():
    ct = datetime.datetime.now()
    print("Time: ", ct)


def myPosition():
    position = client.Positions.Positions_myPosition(symbol="BTCUSD").result()
    print(position)


def returnOrderID():
    print(orderId)


def changeStopLoss(symbol, subtract):
    stop_loss = str(btcLastPrice() - subtract)
    client.Positions.Positions_tradingStop(
        symbol=symbol, stop_loss=stop_loss).result()
    print("Current Price: " + str(btcLastPrice()))
    print("Stop at: " + stop_loss)


# def cancelOrder(orderId, symbol):
#     client.LinearOrder.LinearOrder_cancel(
#         symbol="BTCUSD", order_id=orderId).result()

def closePosition(symbol, amount):
    flag = True
    stopLossInputPrice = btcLastPrice()
    print("Forcing Close")
    changeStopLoss(symbol, amount)
    time.sleep(5)

    while(flag == True):
        if(activePositionCheck(symbol) == 1):
            if (btcLastPrice() > stopLossInputPrice):
                stopLossInputPrice = btcLastPrice()
                print("")
                print("Forcing Close")
                timeStamp()
                changeStopLoss(symbol, amount)
                time.sleep(5)
        else:
            print("Position Closed")
            flag = False


def activeOrderCheck(symbol):
    global orderId
    activeOrder = client.Order.Order_query(symbol=symbol).result()
    order = activeOrder[0]['result']
    if (order == []):
        print("no active orders")
        return 0
    else:
        orderId = order[0]['order_id']
        return 1


# def activeOrderPrice(price):
#     activeOrder = client.Order.Order_query(symbol=symbol).result()
#     order = activeOrder[0]['result']
#     print(order)


def activePositionCheck(symbol):
    position = client.Positions.Positions_myPosition(symbol=symbol).result()
    positionResult = position[0]['result']
    positionValue = positionResult['position_value']
    if(positionValue != "0"):
        return 1
    else:
        return 0


def placeLongOrder(side, symbol, order_type, price):
    global orderId
    stop_loss = btcLastPrice() - 400
    try:
        print(
            f"sending order {price} - {side} {symbol} {order_type} {stop_loss}")
        order = client.Order.Order_new(side=side, symbol=symbol, order_type=order_type,
                                       qty=1, price=price, time_in_force="PostOnly", stop_loss=stop_loss).result()
        orderId = str(order[0]['result']['order_id'])
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return order


def createOrder(side, symbol, order_type, price):
    global orderPrice
    flag = False
    while(flag == False):
        if ((activeOrderCheck(symbol) == 0) and (activePositionCheck(symbol) == 0)):
            print("Attempting to place order...")
            placeLongOrder(side=side, symbol=symbol,
                           order_type=order_type, price=price)
            orderPrice = price
        else:
            forceOrder(symbol, orderId, price)
            print("")
            print("Confirming Order...")
            if ((activeOrderCheck(symbol) == 0) and (activePositionCheck(symbol) == 0)):
                print("Order Failed")
            else:
                print("Order Successful")
                flag = True


def changeOrderPrice(symbol, price, orderId):
    global orderPrice
    if (price != orderPrice):
        client.Order.Order_replace(
            symbol=symbol, order_id=orderId, p_r_price=str(price)).result()
        timeStamp()
        print("Updating Order Price")


def forceOrder(symbol, orderId, price):
    flag = False
    currentPrice = btcLastPrice()

    while(flag == False):
        if (activeOrderCheck(symbol) == 1):
            if (btcLastPrice() != currentPrice):
                currentPrice = btcLastPrice()
                price = btcLastPrice() - 0.50
                changeOrderPrice(symbol, price, orderId)
                print("Order Price Updated: " + str(price))
                print("")
            time.sleep(2)
        else:
            flag = True
