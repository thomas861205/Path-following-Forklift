import numpy as np
import time
import serial
import sys,tty,termios
import cv2
import os

# This class get the pushed key on the keyboard
class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

# This function uses _Getch class and a finite state machine to identify pressed key, including English letter and arrow key
def get():
    inkey = _Getch()
    while(1):
        k=inkey()
        if k!='':break
    # Key sequence starts from '\x1b' means arrow key is pressed, and the arrow direction is stored into the third character (k3)
    if k=='\x1b':
        k2 = inkey()
        k3 = inkey()
        return k3
    else:
        return k

# Object instantiation, creating camera and UART object
dir_name = "../mydata"
vc = cv2.VideoCapture(0)
if os.path.exists( dir_name ) == False:
    raise Exception( dir_name + " does not exist. Please run 'mkdir img' first")

img_counter = 0

while 1:
    print("Press some key...")
    arrow = get()
    if arrow == 'q':
        break
    time.sleep(.2)
    for i in range(5):
       _, img = vc.read()

    _, img = vc.read()
    filename = dir_name + "/" + str(int(time.time()))+".jpg"
    cv2.imwrite( filename, img )
    print( "Img #", img_counter, ": ", filename, " is written" )
