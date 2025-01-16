import math
from common import exec_hpgl

angle_even = math.radians(30)  # angle for even numbers
angle_odd = math.radians(-60)  # angle for odd numbers
scale = 20  # scale for step size (plotter dependent)

# start point in plotter units
# plotter goes from bottom left corner to upper right corner
# (0, 0) to (8636, 11176)
# plotter unit is approximately 1 PU = 0.025 mm (40 PUs per mm resolution)


start_x, start_y = 4000, 4000

def collatz(n):
    if n % 2 == 0:
        return n // 2
    else:
        return (3 * n + 1)

# generate collatz path for a single number
def generate_collatz_path(n):
    x, y = start_x, start_y
    path = [(x, y)]

    while n != 1:
        if n % 2 == 0:
            angle = angle_even
        else:
            angle = angle_odd

        n = collatz(n)
        x += scale * math.cos(angle)
        y += scale * math.sin(angle)
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
        x = max(0, min(x, 8636))
        y = max(0, min(y, 11176))
        instructions.append(f"PD{int(x)},{int(y)};")
    instructions.append("PU;")  # pen up
    return instructions


if __name__ == "__main__":
    port = "/dev/tty.usbserial-10"
    speed = 9600


    hpgl_commands = [
        "IN;",  # initialize plotter
        "SP1;",  # select pen 1
    ]

    # generate collatz paths and plotter commands
    for n in range(2, 10000):
        path = generate_collatz_path(n)
        hpgl_commands.extend(generate_hpgl_path(path))
    hpgl_commands.append("SP0;")  # Deselect pen
    hpgl_commands.append("IN;")  # Reset plotter

    exec_hpgl(hpgl_commands, port=port, speed=speed)