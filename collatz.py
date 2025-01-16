import math
from common import exec_hpgl

angle = -math.radians(4)  # angle for double
scalex = 65  # scale for step size (plotter dependent)
scaley = 65  # scale for step size (plotter dependent)

# start point in plotter units 
# ok from experimentation none of this is really true
# plotter goes from bottom left corner to upper right corner
# (0, 0) to (11176, 8636) (
# plotter unit is approximately 1 PU = 0.025 mm (40 PUs per mm resolution)



start_x, start_y = 1000, 5000


def collatz(n):
    if n % 2 == 0:
        return n // 2
    else:
        return (3 * n + 1) // 2

# generate collatz path for a single number
def generate_collatz_path(n):
    x, y = start_x, start_y
    path = [(x, y)]
    current_angle = math.pi / 2 + math.radians(5)

    seq = []
    while n != 1:
        seq.append(n)
        n = collatz(n)
    seq.reverse()

    for i in range(len(seq)):
        if i < len(seq) - 1:
            nextval = seq[i+1]
        else:
            nextval = seq[i]

        if seq[i] * 2 == nextval:
            current_angle += angle * 2
        else:
            current_angle -= angle
        
        x += scalex * math.cos(current_angle)
        y += scaley * math.sin(current_angle)
        path.append((x, y))
    return path

# generate hpgl commands for a given collatz number path
def generate_hpgl_path(path):
    instructions = []

    start_x, start_y = path[0]
    instructions.append(f"PU{int(start_x)},{int(start_y)};")
    # instructions.append("PD;")  # pen down

    for x, y in path[1:]:
        # ensure the coordinates are within the bounding box
        x = max(0, min(x, 9500))
        y = max(0, min(y, 8200))
        instructions.append(f"PD{int(x)},{int(y)};")
    instructions.append("PU;")  # pen up
    return instructions


if __name__ == "__main__":
    port = "/dev/tty.usbserial-10"
    speed = 9600


    hpgl_commands = [
        "IN;",  # initialize plotter
        "SP3;",  # select pen 1
    ]

    # generate collatz paths and plotter commands
    for n in range(10000, 9500, -1):
        path = generate_collatz_path(n)
        hpgl_commands.extend(generate_hpgl_path(path))
    hpgl_commands.append("SP0;")  # Deselect pen
    hpgl_commands.append("IN;")  # Reset plotter

    exec_hpgl(hpgl_commands, port=port, speed=speed)