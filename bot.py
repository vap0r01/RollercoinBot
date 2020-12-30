import os
import sys
import random
import time
import datetime

import cv2
import keyboard
import mouse
import pyautogui
import shutil
from PIL import ImageGrab
from MTM import matchTemplates, findMatches

GAME_NUM = 0
START_TIME = datetime.datetime.now()


def mouse_click(x, y, wait=0.1, duration=0):
    pyautogui.click(x, y)
    """
    m_pos = mouse.get_position()
    mouse.drag(m_pos[0], m_pos[1], x, y, absolute=True, duration=duration)
    time.sleep(wait)
    print("Click!")
    mouse.click("left")"""


def screen_grab():
    im = ImageGrab.grab()
    img_name = os.getcwd() + "\\imgs\\full_snap__" + str(int(time.time())) + ".png"
    im.save(img_name, "PNG")
    return img_name


def find_image(image_path, root_image_path):
    image = cv2.imread(image_path)
    root_image = cv2.imread(root_image_path)
    method = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCOEFF][0]
    result = cv2.matchTemplate(image, root_image, method)
    mn, _, mn_loc, _ = cv2.minMaxLoc(result)
    if mn > 0.01:
        return None, None
    mp_x, mp_y = mn_loc
    return mp_x, mp_y


def check_image(img):
    b, _ = find_image(img, screen_grab())
    return True if b is not None else False


def click_image(img):
    time.sleep(0.1)
    x, y = find_image(img, screen_grab())
    if x is None or y is None:
        return

    im = cv2.imread(img)
    t_cols, t_rows, _ = im.shape
    mouse_click(x + t_rows * (3 / 5), y + t_cols * (2 / 3))


def setup():
    try:
        os.mkdir('imgs')
    except FileExistsError:
        print("Program was not correctly closed last time. Make sure to exit the game with CTRL+C")


def start_game(start_img_path):
    while not check_image(start_img_path):
        time.sleep(5)
    click_image(start_img_path)
    while not check_image("rc_items/start_game.png"):
        time.sleep(1)
    sx, sy = find_image("rc_items/start_game.png", screen_grab())
    mouse_click(sx + 2, sy + 2, wait=0.1)
    time.sleep(3)


def start_game_msg(name):
    print("Starting Game #{!s}: '{}'@{!s}".format(GAME_NUM, name, datetime.datetime.now().time()))


def end_game():
    while not check_image("rc_items/gain_power.png"):
        time.sleep(1)
    click_image("rc_items/gain_power.png")

    keyboard.press_and_release("page up")

    while not check_image("rc_items/choose_game.png") or check_image("rc_items/collect_pc.png"):
        time.sleep(4)
    if check_image("rc_items/collect_pc.png"):
        click_image("rc_items/collect_pc.png")
        print("PC upgraded!")
        time.sleep(2)
    while check_image("rc_items/choose_game.png"):
        click_image("rc_items/choose_game.png")
        time.sleep(2)


class Bot2048:
    def __init__(self):
        self.start_img_path = "rc_items/2048_gameimg.png"
        self.available_moves = ["right", "left", "up", "down"]
        self.game = "2048"

    def play(self):
        start_game(self.start_img_path)
        start_game_msg(self.game)
        self.run_game()
        end_game()

    def run_game(self):
        while not check_image("rc_items/gain_power.png"):
            for _ in range(4):
                keyboard.press_and_release(random.choice(self.available_moves))
                time.sleep(0.25)


class BotCoinFlip:
    def __init__(self):
        self.start_img_path = "rc_items/coinflip_gameimg.png"
        self.game = "CoinFlip"
        self.coin_pos = []
        self.coin_item = {
            "binance": [],
            "btc": [],
            "eth": [],
            "litecoin": [],
            "monero": [],
            "eos": [],
        }
        self.coin_images = [
            ("binance", cv2.imread("rc_items/coinflip_item_binance.png")),
            ("btc", cv2.imread("rc_items/coinflip_item_btc.png")),
            ("eth", cv2.imread("rc_items/coinflip_item_eth.png")),
            ("litecoin", cv2.imread("rc_items/coinflip_item_litecoin.png")),
            ("monero", cv2.imread("rc_items/coinflip_item_monero.png")),
            ("eos", cv2.imread("rc_items/coinflip_item_eos.png")),
        ]

    def play(self):
        #start_game(self.start_img_path)
        #start_game_msg(self.game)
        self.get_coin_fields()
        self.check_coins()
        self.match_coins()
        #end_game()

    def get_coin_fields(self):
        matches = matchTemplates(
            [("card", cv2.imread("rc_items/coinflip_back.png"))],
            cv2.imread(screen_grab()),
            N_object=float("inf"),
            score_threshold=0.5,
            #maxOverlap=0.25,
            searchBox=None)['BBox']
        for i in range(len(matches)):
            self.coin_pos.append(matches[i])

    def check_coins(self):
        print(len(self.coin_pos))
        pos = 0
        max_index = len(self.coin_pos)-1
        while pos < max_index:
            c1 = self.coin_pos[pos]
            c1_item = None
            mouse_click(c1[0], c1[1], wait=0.3, duration=1)
            match = matchTemplates(
                self.coin_images,
                cv2.imread(screen_grab()),
                N_object=float("inf"),
                score_threshold=.1,
                maxOverlap=.25,
                searchBox=c1)
            print(match)
            if len(match['BBox']) >= 1:
                c1_item = match["TemplateName"][0]
                self.coin_item[c1_item].append(c1)
                break
            pos += 1
            time.sleep(.3)

            c2 = self.coin_pos[pos]
            c2_item = None
            mouse_click(c2[0] + c2[2] / 2, c2[1] + c2[3] / 2, wait=0.3, duration=1)
            match = matchTemplates(
                self.coin_images,
                cv2.imread(screen_grab()),
                N_object=float("inf"),
                score_threshold=.1,
                maxOverlap=.25,
                searchBox=c2)
            print(match)
            if len(match['BBox']) >= 1:
                c2_item = match["TemplateName"][0]
                self.coin_item[c2_item].append(c2)
                break
            pos += 1
            time.sleep(.3)

            if not c1_item:
                print("An error occurred: No matching coin! C1 missing")
                #sys.exit()

            if not c2_item:
                print("An error occurred: No matching coin! C2 missing")
                #sys.exit()

            if c1_item == c2_item and c1_item is not None:
                self.coin_item.pop(c1_item)

            time.sleep(.5)

    def match_coins(self):
        for coin in self.coin_item.values():
            c1 = coin[0]
            mouse_click(c1[0] + c1[2] / 2, c1[1] + c1[3] / 2, wait=0.05)
            c2 = coin[1]
            mouse_click(c2[0] + c2[2] / 2, c2[1] + c2[3] / 2, wait=0.05)
            time.sleep(2)


def main():
    global GAME_NUM
    while True:
        GAME_NUM += 1
        BotCoinFlip().play()
        time.sleep(20)


if __name__ == "__main__":
    setup()
    try:
        bot = BotCoinFlip()
        bot.play()
        #main()

    except KeyboardInterrupt:
        print("Program closed by User!")

    finally:
        print("\nStatistics:\n",
              "Time running: {!s}\n".format(datetime.datetime.now()-START_TIME),
              "Played Games:  {!s}\n".format(GAME_NUM)
              )
        # shutil.rmtree('imgs')
