import os
import sys

def auto_tune_area():
    w, h = os.popen("xdpyinfo | grep dimensions | awk '{print $2;}'").read().split('x')
    tune_area(w, h)

def tune_area(screen_w, screen_h):
    screen_w = float(screen_w)
    screen_h = float(screen_h)
    with os.popen('xsetwacom --set 8 ResetArea; xsetwacom --get 8 area') as f:
        x0, y0, x1, y1 = [int(s) for s in f.read().split()]
    if float(x1) / y1 > screen_w / screen_h:
        new_w = y1 / screen_h * screen_w
        new_x0 = (x1 - new_w) / 2.0
        new_x1 = new_x0 + new_w
        new_y0, new_y1 = y0, y1
    else:
        new_h = x1 / screen_w * screen_h
        new_y0 = (y1 - new_h) / 2.0
        new_y1 = new_y0 + new_h
        new_x0, new_x1 = x0, x1
    os.system('xsetwacom --set 8 area %d %d %d %d' % (new_x0, new_y0, new_x1, new_y1))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        auto_tune_area()
    else:
        if sys.argv[1] == '-i':
            w = int(raw_input("screen width: "))
            h = int(raw_input("screen height: "))
            tune_area(w, h)
        else:
            print("Usage:\n  Auto mode:\t%s\nInteractive:\t%s -i")

