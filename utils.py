import pyautogui
import time
import mss
import mss.tools
import re
import json
import os
from PIL import Image
import pytesseract
from pathlib import Path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
#pyautogui.PAUSE = 0.01

def writeJson(data, filepath):
    with open(filepath, "w+") as outfile:
        outfile.write(json.dumps(data, indent=2))
        outfile.close()

def readJson(filepath):
    f = Path(filepath)
    if f.is_file():
        with open(f, "r") as ff:
            items = json.load(ff)
            ff.close()
            return items

BASE_RES_W = 2560
BASE_RES_H = 1440
CURR_RES_W = pyautogui.size().width
CURR_RES_H = pyautogui.size().height
def focusDiablo():
    win = pyautogui.getWindowsWithTitle('Diablo Immortal')
    win[0].activate()
    pyautogui.moveTo(win[0].center)

def scale(x, y):
    x1 = (x / BASE_RES_W) * CURR_RES_W
    y1 = (y / BASE_RES_H) * CURR_RES_H
    return int(x1), int(y1)

def click(x, y):
    pyautogui.moveTo(scale(x,y))
    pyautogui.click()
    time.sleep(0.1)

def capture(region, save=False):
    with mss.mss() as sct:
        reg = { 'left': region[0], 'top': region[1], 'width': region[2], 'height': region[3] }
        img = sct.grab(reg)
        img2 = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
        if save:
            img2.save("test.png")
        return img2
        #mss.tools.to_png(img.rgb, img.size, output=name)

def nums(s):
    i = 0
    try:
        i = int(re.findall(r'\d+|$', s)[0] or 0)
    except Exception:
        i = 0
    return i

def captureText(left, top, width, height, config = '-c tessedit_char_whitelist=\(\)0123456789abcdefghijklmnopqrstuvwxyz\ ABCDEFGHIJKLMNOPQRSTUVWXYZ%.:+'):
    l, t = scale(left, top)
    w, h = scale(width, height)
    img = capture((l,t,w,h))
    return pytesseract.image_to_string(img, config=config).strip()