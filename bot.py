import os
import random
import time
import datetime

import cv2
import keyboard
import mouse
import shutil
from PIL import ImageGrab

GAME_NUM = 0
START_TIME = datetime.datetime.now()


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
    mn, _, mnLoc, _ = cv2.minMaxLoc(result)
    if mn > 0.01:
        return None, None
    MPx, MPy = mnLoc
    return MPx, MPy


def check_image(img):
    b, _ = find_image(img, screen_grab())
    return True if b is not None else False


def click_image(img):
    time.sleep(0.1)
    x, y = find_image(img, screen_grab())
    if x is None or y is None:
        return
    mpos = mouse.get_position()

    im = cv2.imread(img)
    trows, tcols = im.shape[:2]

    mouse.drag(mpos[0], mpos[1], x + tcols * (3 / 5), y + trows * (2 / 3), absolute=True, duration=0)
    time.sleep(0.2)
    mouse.click("left")


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
    mpos = mouse.get_position()
    mouse.drag(mpos[0], mpos[1], sx + 2, sy + 2, absolute=True, duration=0)
    mouse.click("left")
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


def main():
    global GAME_NUM
    while True:
        GAME_NUM += 1
        Bot2048().play()
        time.sleep(20)


if __name__ == "__main__":
    setup()

    try:
        main()

    except KeyboardInterrupt:
        print("Program closed by User!")

    finally:
        print("\nStatistics:\n",
              "Time running: {!s}\n".format(datetime.datetime.now()-START_TIME),
              "Played Games:  {!s}\n".format(GAME_NUM)
              )
        shutil.rmtree('imgs')
