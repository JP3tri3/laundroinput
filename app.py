import threading
import config
import bybit_info
from time import time, sleep
import json
import time
import datetime
import bybit
import sys
from sanic import Sanic
from sanic import response
from sanic.request import Request
# from sanic.response import json
from sanic_jinja2 import SanicJinja2

# app = Sanic(__name__)
# jinja = SanicJinja2(app, pkg_name="app")

myTime = int(time.time() * 1000)

client = bybit.bybit(test=True, api_key=config.BYBIT_TESTNET_API_KEY,
                     api_secret=config.BYBIT_TESTNET_API_SECRET)

flag = True
orderId = ""


def timeStamp():
    ct = datetime.datetime.now()
    print("Time: ", ct)


def shutdown():
    print("")
    print("Shutting down...")
    sys.exit("Program Terminated")
    print("")


def inputOptions():
    print("")
    print("Input Options:")
    print("Create Long Order: 'long'")
    print("BTC Price info: 'btc price'")
    print("BTC Info: 'btc info'")
    print("BTC Wallet: 'btc wallet'")
    print("Eth Wallet: 'eth wallet'")
    print("Active Orders: 'active order'")
    print("Position: 'position'")
    print("Cancel Orders: 'cancel orders'")
    print("Stop Loss: 'stoploss'")
    print("Market Close: 'close'")
    print("Order Id: 'order id'")
    print("Exit: 'exit'")


def cancelOrder(orderId, symbol):
    client.LinearOrder.LinearOrder_cancel(
        symbol="BTCUSD", order_id=orderId).result()


def placeLongOrder(side, symbol, order_type, price):
    global orderId
    stop_loss = bybit_info.btcLastPrice() - 400
    try:
        print(
            f"sending order {price} - {side} {symbol} {order_type} {stop_loss}")
        order = client.Order.Order_new(side=side, symbol=symbol, order_type=order_type,
                                       qty=1, price=price, time_in_force="PostOnly", stop_loss=stop_loss).result()
        orderId = str(order[0]['result']['order_id'])
        print(orderId)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return order


def main():
    global flag

    inputOptions()

    while(flag == True):

        print("")
        taskInput = input("Input Task: ")
        timeStamp()

        if(taskInput == "exit"):
            shutdown()

        elif(taskInput == "btc price"):
            bybit_info.btcPriceInfo()

        elif(taskInput == "btc info"):
            bybit_info.btcInfo()

        elif(taskInput == "long"):
            order_response = placeLongOrder(
                "Buy", "BTCUSD", "Limit", bybit_info.btcLastPrice() - 0.50)
            if order_response:
                print("Order Successful")
            else:
                print("Order Failed")

        elif(taskInput == "btc wallet"):
            bybit_info.btcWallet()

        elif(taskInput == "eth wallet"):
            bybit_info.ethWallet()

        elif(taskInput == "active order"):
            print(bybit_info.activeOrder())

        elif(taskInput == "stoploss"):
            bybit_info.changeStopLoss("BTCUSD", 500)
            print("Updated Stop Loss")

        elif(taskInput == "close"):
            bybit_info.changeStopLoss("BTCUSD", 10)
            print("Updated Stop Loss")

        elif(taskInput == "cancel orders"):
            bybit_info.cancelAllOrders("BTCUSD")
            print("Orders Cancelled")

        elif(taskInput == "order id"):
            print("Order ID: " + orderId)

        elif(taskInput == "position"):
            print("Position: ")
            bybit_info.myPosition()

        else:
            print("Invalid Input, try again...")
            inputOptions()


# def priceTest():
#     while(flag == True):
#         timeStamp()
#         info = client.Market.Market_symbolInfo().result()
#         keys = info[0]['result']
#         btcInfo = keys[0]['last_price']
#         print(btcInfo)
#         sleep(1)


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)


main()
