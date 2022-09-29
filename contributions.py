from utils import *
import time
import re
import pandas as pd
import pyautogui

def nextDown():
    #pyautogui.moveTo(1280, 720)
    time.sleep(0.1)
    for i in range(0,2):
        pyautogui.scroll(-1)
    time.sleep(0.2)

def scrapeContributions():
    
    DELTA_Y = 170
    items = []
    
    focusDiablo()
    def scrapeDetails(row, item = {}):
        click(1932, 489 + row * DELTA_Y)
        boxY = 509 + row * DELTA_Y
        if row == 4:
            boxY = 1146
        txt = captureText(1095,boxY,592,213).strip()
        pyautogui.rightClick()

        for line in txt.split("\n"):
            arr = line.replace("- ", "").split(': ')
            if len(arr) > 1:
                key, value = line.replace("- ", "").split(': ')
                item[key] = nums(value)
        return item
                
    def scrapeItem(row = 0, item = {}):
        if row <= 0:
            row = 0

        name, level = re.split("\n?Rank:?",captureText(913,421 + row * DELTA_Y,317,116))
        item['name'] = name.replace('-', '').replace('.', '')
        role = captureText(1322,414 + row * DELTA_Y,470,140)
        item['role'] = role
        lastOnline = captureText(2107,418 + row * DELTA_Y,355,125)
        item['lastOnline'] = lastOnline
        item['level'] = level.strip()     
        return item
    def saveItem(newItem):
        if not next((item for item in items if item["name"] == newItem["name"]), False):
            items.append(newItem)
            writeJson(items, "contributions.json")
            print('saved', newItem['name'])
    items = readJson("contributions.json") or []
    
    for n in range(0, 295):
        item = {}
        if n == 0:
            scrapeItem(0, item)
            scrapeDetails(0, item)
            nextDown()
        else:
            scrapeDetails(1, item)
            nextDown()
            scrapeItem(0, item)
        print(item)
        saveItem(item)
        
    for n in range(0, 5):
        item = {}
        scrapeItem(n, item)
        scrapeDetails(n, item)
        print(item)
        saveItem(item)

    print(items)
    df = pd.read_json("contributions.json")
    df.to_csv("contributions.csv")

scrapeContributions()
#df = pd.read_json("contributions.json")
#df.to_csv("contributions.csv")