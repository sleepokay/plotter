import math
import random
from collections import namedtuple
import time

import numpy as np

from common import exec_hpgl

def dragon():
    instructions = []
    s = "A"
    for _ in range(0,5):
        ns = ""
        for c in s:
            if c == "A":
                ns += "-BF+AFA+FB-"
            elif c == "B":
                ns += "+AF-BFB-FA+"
            else:
                ns += c
        s = ns

    instructions.append("PU;SP1;PA3000,5000;PD;")

    angle = 0
    moves = ["PR 100,0;", "PR 0,100;", "PR -100,0;", "PR0,-100;"]
    for c in s:
        if c == "+":
            angle = (angle+1)%4
        elif c == "-":
            angle = (angle-1)%4
        elif c == "F":
            instructions.append(moves[angle])
    instructions.append("SP0;")
    return instructions

if __name__ == "__main__":
    port = "/dev/tty.usbserial-10"
    speed = 9600

    instructions = dragon()

    # write_hpgl(instructions, "images/polygons.hpgl")
    time.sleep(2) 
    exec_hpgl(instructions, port=port, speed=speed)
