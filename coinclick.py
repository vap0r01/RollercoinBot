import os
import random
import time
import datetime

import cv2
import keyboard
import mouse
import shutil
from PIL import ImageGrab
import pyautogui, time , keyboard, random, win32api, win32con
time.sleep(3)
def click(x,y):
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

gameover = False

while 1:
    time.sleep(3)

    if pyautogui.locateOnScreen('rc_items/CoinClickGame.png', confidence=0.9) != None:
        image = pyautogui.locateOnScreen('rc_items/CoinClickGame.png', confidence=0.8)
        x, y = pyautogui.center(image)
        pyautogui.moveTo(x+5, y+20)
        pyautogui.click()
        gameover = False
        time.sleep(5)


    if pyautogui.locateOnScreen('rc_items/start_game.png', confidence=0.9) != None:
        image = pyautogui.locateOnScreen('rc_items/start_game.png', confidence=0.8)
        x, y = pyautogui.center(image)
        pyautogui.moveTo(x+5, y+20)
        pyautogui.click()
        time.sleep(3)



    while gameover == False:
        pic = pyautogui.screenshot(region=(530, 430, 828, 417,))
        width, height = pic.size
        for x in range(0, width, 5):
            for y in range(0, height, 5):

                r, g, b = pic.getpixel((x, y))

                # blue coin
                if b == 183 and r == 0:
                    click(x + 530, y + 440)
                    print("blue coin click")

                    break

                # yellow coin
                if b == 64 and r == 200:
                    click(x + 530, y + 440)
                    print("yellow coin click")

                    break

                    # orange coin
                if b == 33 and r == 231:
                    click(x + 530, y + 440)
                    print("orange coin click")

                    break

                # grey coin
                if b == 230 and r == 230:
                    click(x + 535, y + 440)
                    print("grey coin click")

                    break

                # game finish button
                if b == 228 and r == 3:
                    time.sleep(3)
                    click(x + 530, y + 435)
                    print("game finish click taking 10 sec wait while verifying")

                    gameover = True
                    print("Game Over = " + str(gameover))
                    time.sleep(15)


                    break

            if gameover == True:
                break
        if gameover == True:
            break

    print("exit from for loop")

    if pyautogui.locateOnScreen('rc_items/choose_game.png', confidence=0.9) != None:
        image = pyautogui.locateOnScreen('rc_items/choose_game.png', confidence=0.8)
        x, y = pyautogui.center(image)
        pyautogui.moveTo(x, y)
        pyautogui.click()
        time.sleep(5)

    print("taking 20 seconds break")
    time.sleep(20)

