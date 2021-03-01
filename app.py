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
    print("Active Orders: 'active'")
    print("Position: 'position'")
    print("Cancel Orders: 'cancel'")
    print("Change Order: 'change'")
    print("Stop Loss: 'stoploss'")
    print("Market Close: 'close'")
    print("Order Id: 'order id'")
    print("Exit: 'exit'")


def main():
    global flag

    inputOptions()

    while(flag == True):

        print("")
        taskInput = input("Input Task: ")
        bybit_info.timeStamp()

        if(taskInput == "exit"):
            shutdown()

        elif(taskInput == "btc price"):
            bybit_info.btcPriceInfo()

        elif(taskInput == "btc info"):
            bybit_info.btcInfo()

        elif(taskInput == "long"):
            bybit_info.createOrder("Buy", "BTCUSD", "Limit",
                                   bybit_info.btcLastPrice() - 50)

        elif(taskInput == "btc wallet"):
            bybit_info.btcWallet()

        elif(taskInput == "eth wallet"):
            bybit_info.ethWallet()

        elif(taskInput == "active"):
            print(bybit_info.activeOrderCheck())

        elif(taskInput == "stoploss"):
            bybit_info.changeStopLoss("BTCUSD", 500)
            print("Updated Stop Loss")

        elif(taskInput == "close"):
            bybit_info.closePosition("BTCUSD", 2)

        elif(taskInput == "change"):
            bybit_info.activeOrderCheck()
            bybit_info.changeOrderPrice(
                "BTCUSD", bybit_info.btcLastPrice() - 0.50, orderId)

        elif(taskInput == "cancel"):
            bybit_info.cancelAllOrders("BTCUSD")
            print("Orders Cancelled")

        elif(taskInput == "order id"):
            print("Order ID: ")
            bybit_info.returnOrderID()

        elif(taskInput == "position"):
            print("Position: ")
            # bybit_info.myPosition()
            print(bybit_info.activePositionCheck())

        elif(taskInput == "test"):
            bybit_info.activeOrderPrice("BTCUSD")

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
