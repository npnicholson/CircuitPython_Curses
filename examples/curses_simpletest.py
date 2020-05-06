""" Simple test file for the curses framework
"""

import sys
import time


import supervisor
from circuitpython_curses import curses

# print("\33[0m", end="")


# st = "\33[38;5;55;48;5;196mthis is a test!\33[0m"

# print(curses.clean_ansi(st).encode())

# #

# # print("\33[38;5;55;48;5;196mthis is a test!")
# # print("\33[38;2;0;128;128mthis is a test!")


# # print("\33[30;47mthis is a test!")
# # print("\33[38;5;27mthis is a test!", end="")

# # print("\33[38;5;27mThis is a test!")


# sys.exit()

try:
    curses.curs_set(1)
    STDSCR = curses.initscr()

    curses.init_pair(1, 207, -1)
    curses.init_pair(2, -1, 123)
    curses.init_pair(3, 207, 123)
    curses.init_pair(4, -1, -1)
    curses.init_pair(5, curses.COLOR_RED, -1)

    for y in range(0, STDSCR.getmaxyx()[0]):
        for x in range(0, STDSCR.getmaxyx()[1] - 1):
            STDSCR.addstr(y, x, "#")
            STDSCR.refresh()

    for y in range(0, STDSCR.getmaxyx()[0]):
        for x in range(0, STDSCR.getmaxyx()[1] - 1):
            STDSCR.addstr(y, x, ".")
            STDSCR.refresh()

    for y in range(0, STDSCR.getmaxyx()[0]):
        for x in range(0, STDSCR.getmaxyx()[1] - 1):
            STDSCR.addstr(y, x, " ")
            STDSCR.refresh()

    STDSCR.addstr(9, 10, "A")
    STDSCR.addstr(10, 9, "B")

    STDSCR.addstr(19, 9, "C")  # 20, 9
    STDSCR.addstr(20, 10, "D")  # 21, 10

    STDSCR.addstr(20, 29, "E")  # 21, 30
    STDSCR.addstr(19, 30, "F")  # 20, 31

    STDSCR.addstr(10, 30, "G")  # 10, 31
    STDSCR.addstr(9, 29, "H")  # 9,  30

    STDSCR.addstr(9, 42, "#:   Wx  h     x, y")
    STDSCR.addstr(10, 40, "Win: (10, 20)  (10, 10)")

    STDSCR.addstr(12, 42, "A:           ( 9, 10)", curses.color_pair(1))
    STDSCR.addstr(13, 42, "B:           (10,  9)", curses.color_pair(2))
    STDSCR.addstr(14, 42, "C:           (19,  9)", curses.color_pair(3))
    STDSCR.addstr(15, 42, "D:           (20, 10)")
    STDSCR.addstr(16, 42, "E:           (20, 29)")
    STDSCR.addstr(17, 42, "F:           (19, 30)")
    STDSCR.addstr(18, 42, "G:           (10, 30)")
    STDSCR.addstr(19, 42, "H:           ( 9, 29)")

    STDSCR.addstr(2, 3, f"Window Size: {STDSCR.getmaxyx()}")

    STDSCR.box()

    WIN = curses.newwin(10, 20, 10, 10)
    WIN.box()

    WIN.addstr(1, 8, "Win")
    WIN.addstr(1, 1, "1")
    WIN.addstr(1, 18, "2")
    WIN.addstr(8, 18, "3")
    WIN.addstr(8, 1, "4")

    WIN.addstr(3, 6, "1: 1, 1")
    WIN.addstr(4, 6, "2: 1,18")
    WIN.addstr(5, 6, "3: 8,18")
    WIN.addstr(6, 6, "4: 8, 1")

    STDSCR.addstr(11, 40, f"Pos: {WIN.getmaxyx()}  {WIN.getbegyx()} ")

    WIN.refresh()

    WIN2 = curses.newwin(5, 5, 20, 40)
    WIN2.box()

    # WIN2.addstr(0, 1, "ABC")
    WIN2.addstr(1, 1, "ABC")
    WIN2.addstr(2, 1, "ABC")
    WIN2.addstr(3, 1, "ABC")

    WIN3 = curses.newwin(6, 20, 25, 10)
    WIN3.box()

    # WIN3.addstr(
    #     0,
    #     0,
    #     "0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123456789abcdefghijklmnopqrstuvwxyz0123456789a",
    # )

    # WIN3.addstr(
    #     0,
    #     0,
    #     "0123456789abcdefghijklmnopqrstuvwxyz012345678uvwxyz\nThis is a test! and so is \nthis and bla",
    #     curses.color_pair(5),
    # )

    WIN3.addstr(
        0, 0, "▆" * 35 + "\n" + "▆" * 20, curses.color_pair(5),
    )

    WIN3.refresh()

    WIN4 = curses.newwin(6, 20, 32, 10)
    WIN4.box()

    WIN4.addstr(
        0,
        0,
        "0123456789abcdefghijklmnopqrstuvwxyz012345678uvwxyz\nThis is a test! and so is \nthis and bla",
        curses.color_pair(5),
    )

    WIN4.refresh()

    _color = 0
    for y in range(0, STDSCR.getmaxyx()[0]):
        for x in range(80, STDSCR.getmaxyx()[1] - 2):
            STDSCR.addstr(y, x, "#", (_color % 256))
            _color = _color + 1
            STDSCR.refresh()


finally:
    curses.curs_set(0)
    curses.endwin()

while not supervisor.runtime.serial_bytes_available:
    time.sleep(0.01)

sys.exit()
