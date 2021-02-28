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

flag = True


def inputOptions():

    print("")
    print("Input Options:")
    print("btc price | BTC Price info")
    print("exit | Exit")
    print("")


def main():
    global flag

    inputOptions()

    while(flag == True):
        taskInput = input("Input Task: ")
        print("response is: " + taskInput)

        if(taskInput == "exit"):
            print("Shutting down...")
            sys.exit("Program Terminated")
        elif(taskInput == "btc price"):
            getPriceInfo()
        else:
            print("Invalid Input, try again...")
            inputOptions()


def getPriceInfo():
    print("Last Price: " + bybit_info.btcLastPrice)
    print("Mark Price: " + bybit_info.btcMarkPrice)
    print("Ask Price: " + bybit_info.btcAskPrice)
    print("Index Price: " + bybit_info.btcIndexPrice)


def timeStamp():
    ct = datetime.datetime.now()
    print("Time: ", ct)

# for i in btcInfo:
#     print(i)
#     print("")


flag = True

# while(flag == True):
#     if (bybit_info.btcLastPrice > 45000):
#         timeStamp()
#         print("BTC > 45000")
#         sleep(1)
#     else:
#         timeStamp()
#         print("BTC < 45000")
#         sleep(1)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000, debug=True)

main()
