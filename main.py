# %%
import pyautogui
import keyboard
import glob
from math import floor
from time import sleep, perf_counter
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

# %%
files = glob.glob("*.osu")
hit = []
executor = ThreadPoolExecutor(max_workers=15)

def load_osu():

    for file in files:
        with open(file, "r", encoding="utf8") as f:
            content = f.readlines()

    global hitObject, CircleSize
    hitObject = content[(content.index("[HitObjects]\n")) + 1:]
    hitObject = [s.strip() for s in hitObject]
    CircleSize = int(content[content.index("[Difficulty]\n") + 2].split(":")[1])


    for obj in hitObject:
        parts = obj.split(",")
        isLN = True if int(parts[3]) == 128 else False

        info = {
            "hitPos": int(parts[0]),
            "timing": int(parts[2]),
            "isLN": isLN,
            "LNrelease": int(parts[5].split(":")[0]) if isLN else None
        }
        hit.append(info)

def play():

    def press(obj):
        if not obj["isLN"]: #飯
            pyautogui.keyDown(obj["hitPos"])
            sleep(0.01) #press 20ms
            pyautogui.keyUp(obj["hitPos"])
        else: #LN
            pyautogui.keyDown(obj["hitPos"])
            sleep((obj["LNrelease"] - obj["timing"]) / 1000.0)
            pyautogui.keyUp(obj["hitPos"])

    for obj in hit:
        if CircleSize == 4:
            if obj["hitPos"] == 64:
                obj["hitPos"] = "d"
            elif obj["hitPos"] == 192:
                obj["hitPos"] = "f"
            elif obj["hitPos"] == 320:
                obj["hitPos"] = "g"
            elif obj["hitPos"] == 448:
                obj["hitPos"] = "h"
        elif CircleSize == 7:
            if obj["hitPos"] == 36:
                obj["hitPos"] = "s"
            elif obj["hitPos"] == 109:
                obj["hitPos"] = "d"
            elif obj["hitPos"] == 182:
                obj["hitPos"] = "f"
            elif obj["hitPos"] == 256:
                obj["hitPos"] = "space"
            elif obj["hitPos"] == 329:
                obj["hitPos"] = "j"
            elif obj["hitPos"] == 402:
                obj["hitPos"] = "k"
            elif obj["hitPos"] == 475:
                obj["hitPos"] = "l"


        
        current = floor(perf_counter()*1000) - start
        if abs(current - obj["timing"]) <= 10:
            executor.submit(press, obj)
            Thread(target=press, args=(obj,)).start()

if __name__ == "__main__":
    load_osu()
    start = floor(perf_counter() * 1000)

    while True:
        if keyboard.is_pressed('m'):
            play()
        elif keyboard.is_pressed('alt'):
            break
        sleep(0.010)


