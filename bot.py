import os
import random
import time

import cv2
import keyboard
import mouse
import shutil
from PIL import ImageGrab

GAME_NUM = 0


def screen_grab():
    im = ImageGrab.grab()
    img_name = os.getcwd() + "\\imgs\\ful_snap__" + str(int(time.time())) + ".png"
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


def start_game():
    start_img_path = "rc_items/2048_gameimg.png"
    while not check_image("rc_items/2048_gameimg.png"):
        time.sleep(5)
    click_image(start_img_path)

    while not check_image("rc_items/start_game.png"):
        time.sleep(1)
    sx, sy = find_image("rc_items/start_game.png", screen_grab())
    mpos = mouse.get_position()
    mouse.drag(mpos[0], mpos[1], sx + 2, sy + 2, absolute=True, duration=0)
    mouse.click("left")


def run_game():
    while not check_image("rc_items/gain_power.png"):
        for _ in range(10):
            keys = ["right", "left", "up", "down"]
            keyboard.press_and_release(random.choice(keys))
            time.sleep(0.1)


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


def main():
    global GAME_NUM
    GAME_NUM += 1
    print("Game #{!s}".format(GAME_NUM))
    start_game()
    run_game()
    end_game()
    time.sleep(30)


try:
    os.mkdir('imgs')
    while True:
        main()

except KeyboardInterrupt:
    pass

finally:
    shutil.rmtree('imgs')
