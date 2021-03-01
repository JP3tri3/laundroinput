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


def timeStamp():
    ct = datetime.datetime.now()
    print("Time: ", ct)


def inputOptions():
    print("")
    print("Input Options:")
    print("Create Long Order: 'buy'")
    print("BTC Price info: 'btc price'")
    print("BTC Info: 'btc info'")
    print("BTC Wallet: 'btc wallet'")
    print("Eth Wallet: 'eth wallet'")
    print("Exit: 'exit'")


def placeOrder(side, symbol, order_type, price):
    try:
        print(f"sending order {price} - {side} {symbol} {order_type}")
        order = client.Order.Order_new(side=side, symbol=symbol, order_type=order_type,
                                       qty=1, price=price, time_in_force="GoodTillCancel").result()

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
            print("Shutting down...")
            sys.exit("Program Terminated")

        elif(taskInput == "btc price"):
            bybit_info.btcPriceInfo()

        elif(taskInput == "btc info"):
            bybit_info.btcInfo()

        elif(taskInput == "buy"):
            order_response = placeOrder(
                "Buy", "BTCUSD", "Limit", bybit_info.btcLastPrice())
            if order_response:
                print("Order Successful")
            else:
                print("Order Failed")

        elif(taskInput == "btc wallet"):
            bybit_info.btcWallet()

        elif(taskInput == "eth wallet"):
            bybit_info.ethWallet()

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
