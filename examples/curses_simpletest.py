""" Simple test file for the curses framework
"""

import sys
import time


import supervisor
from circuitpython_curses import curses

try:
    curses.curs_set(1)
    STDSCR = curses.initscr()

    # stdscr.addstr(0, 0, "#")

    # sys.exit()
    # curses.noecho()

    # stdscr.addstr(9, 10, "@")
    # stdscr.addstr(10, 9, "@")

    # stdscr.addstr(20, 9, "@")
    # stdscr.addstr(21, 10, "@")

    # stdscr.addstr(21, 30, "@")
    # stdscr.addstr(20, 31, "@")

    # stdscr.addstr(10, 31, "@")
    # stdscr.addstr(9, 30, "@")

    for y in range(0, STDSCR.getmaxyx()[0]):
        for x in range(0, STDSCR.getmaxyx()[1]):
            STDSCR.addstr(y, x, "#")
            STDSCR.refresh()

    for y in range(0, STDSCR.getmaxyx()[0]):
        for x in range(0, STDSCR.getmaxyx()[1]):
            STDSCR.addstr(y, x, ".")
            STDSCR.refresh()

    for y in range(0, STDSCR.getmaxyx()[0]):
        for x in range(0, STDSCR.getmaxyx()[1]):
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

    STDSCR.addstr(9, 40, "Win: 10x20 @ 10,10")
    STDSCR.addstr(10, 42, "#:  Wx h    x, y")
    STDSCR.addstr(11, 42, "A:          9,10")
    STDSCR.addstr(12, 42, "B:         10, 9")
    STDSCR.addstr(13, 42, "C:         19, 9")
    STDSCR.addstr(14, 42, "D:         20,10")
    STDSCR.addstr(15, 42, "E:         20,29")
    STDSCR.addstr(16, 42, "F:         19,30")
    STDSCR.addstr(17, 42, "G:         10,30")
    STDSCR.addstr(18, 42, "H:          9,29")

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

    WIN.refresh()

    # for i in range(126, 1000):
    #     STDSCR.addstr(0, 0, chr(i))
    #     # curses.cursor_pos = (
    #     #     curses.cursor_pos[0], curses.cursor_pos[1]+len(chr(i)))
    #     # STDSCR.addstr(1, 0, str(i))
    #     # STDSCR.addstr(2, 0, str(len(chr(i))))
    #     time.sleep(0.01)
    # curses.cursor_pos = (
    # curses.cursor_pos[0], curses.cursor_pos[1]+2)

    # STDSCR.box()

    WIN2 = curses.newwin(5, 5, 20, 40)
    WIN2.box()

    # WIN2.addstr(0, 1, "ABC")
    WIN2.addstr(1, 1, "ABC")
    WIN2.addstr(2, 1, "ABC")
    WIN2.addstr(3, 1, "ABC")

    for y in range(0, STDSCR.getmaxyx()[0]):
        for x in range(81, STDSCR.getmaxyx()[1] - 2):
            STDSCR.addstr(y, x, "#")
            STDSCR.refresh()

    for y in range(0, STDSCR.getmaxyx()[0], 1):
        STDSCR.addstr(y, 3, str(y))
        STDSCR.refresh()

    for x in range(0, STDSCR.getmaxyx()[1], 1):
        STDSCR.addstr(3, x, str(x % 10))
        STDSCR.refresh()

finally:
    curses.curs_set(0)
    curses.endwin()

while not supervisor.runtime.serial_bytes_available:
    time.sleep(0.01)

sys.exit()
