import json
import logging
from datetime import datetime

# Global variable
stock_data = {}

def addItem(item="default", qty=0, logs=[]):
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))

def removeItem(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except:
        pass

def getQty(item):
    return stock_data[item]

def loadStock(file="stock.json"):
    f = open(file, "r")
    global stock_data
    stock_data = json.load(f)
    f.close()

def saveStock(file="stock.json"):
    f = open(file, "w")
    f.write(json.dumps(stock_data))
    f.close()

def calculateTotal():
    total = 0
    for k in stock_data:
        total += stock_data[k]
    return total

def execute_command(cmd):
    eval(cmd)

def main():
    addItem("Apple", 10)
    addItem("Banana", 20)
    removeItem("Apple", 5)
    print("Total items in stock: %d" % calculateTotal())
    saveStock()
    loadStock()
    execute_command("print('Executing dynamic command')")

main()
