import bybit
import config
import json
import time
import datetime

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)

orderId = ""
orderPrice = 0
margin = 5
inputQuantity = 100 * margin
entry_price = 0.0
stop_loss = 0
level = 0
# manual ATR

atr = 0
atr1m = 0
atr3m = 0
atr5m = 0
atr10m = 0
atr15m = 0
atr30m = 0
atr1hr = 0


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


# Order Functions

def cancelAllOrders(symbol):
    client.Order.Order_cancelAll(symbol=symbol).result()


def timeStamp():
    ct = datetime.datetime.now()
    print("Time: ", ct)


def myPosition():
    position = client.Positions.Positions_myPosition(symbol="BTCUSD").result()
    print(position)


def returnOrderID():
    print(orderId)


# Active Checks


def activeOrderCheck(symbol):
    global orderId
    activeOrder = client.Order.Order_query(symbol=symbol).result()
    order = activeOrder[0]['result']
    if (order == []):
        print("no pending orders")
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


def activePositionEntryPrice(symbol):
    position = client.Positions.Positions_myPosition(symbol=symbol).result()
    positionResult = position[0]['result']
    positionEntryPrice = positionResult['entry_price']
    return float(positionEntryPrice)

# Create Functions:


def inputAtr():
    global atr
    flag = False
    print("")
    while(flag == False):
        atr = input("Input ATR: ")
        if(atr.isnumeric()):
            print("ATR input accepted for SL: " + str(atr))
            flag = True
        else:
            print("Invalid Input, try again...")


def placeOrder(side, symbol, order_type, price):
    global orderId
    global entry_price
    entry_price = btcLastPrice()

    if(side == "Buy"):
        stop_loss = btcLastPrice() - float(calculateOnePercentLessEntry())
    else:
        stop_loss = btcLastPrice() + float(calculateOnePercentLessEntry())

    try:
        print(
            f"sending order {price} - {side} {symbol} {order_type} {stop_loss}")
        order = client.Order.Order_new(side=side, symbol=symbol, order_type=order_type,
                                       qty=inputQuantity, price=price, time_in_force="PostOnly", stop_loss=str(stop_loss)).result()
        orderId = str(order[0]['result']['order_id'])
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return order


def changeOrderPrice(symbol, price, orderId):
    global orderPrice
    if (price != orderPrice):
        client.Order.Order_replace(
            symbol=symbol, order_id=orderId, p_r_price=str(price)).result()
        timeStamp()
        print("Updating Order Price")


def forceOrder(symbol, orderId, side):
    flag = False
    currentPrice = btcLastPrice()
    price = limitPriceDifference(side)

    while(flag == False):
        if (activeOrderCheck(symbol) == 1):
            if (btcLastPrice() != currentPrice) and (btcLastPrice() != price):
                print("btcLastPrice: " + str(btcLastPrice()))
                print("currentPrice: " + str(currentPrice))
                print("price: " + str(price))
                currentPrice = btcLastPrice()
                price = limitPriceDifference(side)
                changeOrderPrice(symbol, price, orderId)
                print("Order Price Updated: " + str(price))
                print("")
            time.sleep(2)
        else:
            flag = True


def createOrder(side, symbol, order_type, price):
    global orderPrice
    global entry_price
    flag = False
    inputAtr()

    while(flag == False):
        if ((activeOrderCheck(symbol) == 0) and (activePositionCheck(symbol) == 0)):
            print("Attempting to place order...")
            placeOrder(side=side, symbol=symbol,
                       order_type=order_type, price=limitPriceDifference(side))
            orderPrice = price
        else:
            forceOrder(symbol, orderId, side)
            print("")
            print("Confirming Order...")
            if ((activeOrderCheck(symbol) == 0) and (activePositionCheck(symbol) == 0)):
                print("Order Failed")
            else:
                entry_price = activePositionEntryPrice(symbol)
                print("Entry Price: " + str(entry_price))
                print("Order Successful")
                flag = True

    updateStopLoss(symbol, side)
    print("Entry Price: " + str(entry_price))
    print("Exit Price: " + str(stop_loss))

# Close & Stoploss


def updateStopLoss(symbol, side):
    if(side == "Buy"):
        initialSl = float(activePositionEntryPrice(symbol)) - \
            float(calculateOnePercentLessEntry())
    else:
        initialSl = float(activePositionEntryPrice(symbol)) + \
            float(calculateOnePercentLessEntry())

    changeStopLoss(symbol, initialSl)
    flag = True
    lockPrice = btcLastPrice()

    if(atr == 0):
        inputAtr()

    while (flag == True):
        if(activePositionCheck(symbol) == 1):
            if(side == "Buy"):
                # print(entry_price)
                # print(calculatePercentGained())
                # print(calculateOnePercentDifference())
                if(btcLastPrice() > lockPrice):
                    # updatingStopLoss = btcLastPrice() - float(atr)
                    changeStopLoss(symbol, stop_loss)
                    lockPrice = btcLastPrice()
                    print("Stop Loss: " + str(stop_loss))
                    print("Level: " + str(level))
                    print("")
            else:
                if(btcLastPrice() < lockPrice):
                    updatingStopLoss = btcLastPrice() + float(atr)
                    changeStopLoss(symbol, updatingStopLoss)
                    lockPrice = btcLastPrice()
                    print("")
        else:
            print("Position Closed")
            print("")
            flag = False


def changeStopLoss(symbol, slAmount):
    calculateStopLoss()
    client.Positions.Positions_tradingStop(
        symbol=symbol, stop_loss=str(stop_loss)).result()
    print("")
    print("Current Price: " + str(btcLastPrice()))
    print("Stop at: " + str(stop_loss))


def closePositionSl(symbol):
    flag = True
    stopLossInputPrice = btcLastPrice()
    print("Forcing Close")
    changeStopLoss(symbol, btcLastPrice() - float(2))
    time.sleep(5)

    while(flag == True):
        if(activePositionCheck(symbol) == 1):
            if (btcLastPrice() > stopLossInputPrice):
                stopLossInputPrice = btcLastPrice()
                print("")
                print("Forcing Close")
                timeStamp()
                changeStopLoss(symbol, btcLastPrice() - float(2))
                time.sleep(5)
        else:
            print("Position Closed")
            flag = False


def closePositionMarket(symbol):
    client.Order.Order_new(side="Sell", symbol=symbol, order_type="Market",
                           qty=inputQuantity, time_in_force="GoodTillCancel").result()
    print("Position Closed at: " + str(btcLastPrice()))


def limitPriceDifference(side):
    if(side == "Buy"):
        return str(btcLastPrice() - 0.50)
    else:
        return str(btcLastPrice() + 0.50)


def calculateOnePercentLessEntry():
    onePercentDifference = (float(entry_price) * 0.01) / margin
    print("One percent Difference: " + str(onePercentDifference))
    return onePercentDifference


def calculatePercentGained():
    difference = (btcLastPrice() - float(entry_price))
    percent = (difference/btcLastPrice()) * 100
    percentWithMargin = (percent) * margin
    return float(percentWithMargin)


def calculateStopLoss():
    global level
    global stop_loss
    level = entry_price

    if (calculatePercentGained() < 0.25):
        stop_loss = calculateOnePercentLessEntry()
    elif (calculatePercentGained() >= 0.25) and (calculatePercentGained() < 0.5):
        stop_loss = entry_price
        level = btcLastPrice()
    elif (calculatePercentGained() >= 0.5):
        stop_loss = level
        level = btcLastPrice()
