import sys
import time

import re
import os

import supervisor
from circuitpython_curses import curses, escape

curses.write("\033[2J")

curses.write(escape.cup(2, 2))
# curses.write("\33[0m")

# Move the cursor to 500, 500
# curses.write("\033[500B")
# curses.write("\033[500C")

# Ask the term where the cursor is
curses.write("\033[6n")

# Clear the screen again
# curses.write("\033[2J")

curses.cursor_pos = (0, 0)

# Set up a serial capure unit
counter = 0
done = False
buf = ""
while not done:
    # Add to a counter each time we wait
    counter = counter + 1
    # While there is serial bytes available, read them into our buffer
    while supervisor.runtime.serial_bytes_available:
        # Get the char
        char = sys.stdin.read(1)
        # Read it into the buffer
        buf = buf + char
        # If the char is the escape.RSP char, then we are done
        if (char is escape.RSP):
            done = True
            break

    # Wait for more serial data
    time.sleep(0.01)

    # If we have been waiting too long, fail
    if (counter > 100):
        raise OSError("Unable to get screen size: Timeout")

escape_arguments = escape(buf).get_args()


# curses.write("0")

# curses.write(" -- " + escape_arguments[0] + " " + escape_arguments[1])
# curses.write(str(int(escape_arguments[0]), int(escape_arguments[1])))

# Window size is reduced by 4 because the window cannot extend all the way to
# the right side without causing distortions on UNICODE characters (which have a
# visible length of 1, but a codeunit length of 2):
# https://stackoverflow.com/questions/30775689/python-length-of-unicode-string-confusion
# print((
#     int(escape_arguments[0]), int(escape_arguments[1])))


try:
    curses.curs_set(1)
    stdscr = curses.initscr()

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

    # for y in range(0, stdscr.getmaxyx()[0]):
    #     for x in range(0, stdscr.getmaxyx()[1]):
    #         stdscr.addstr(y, x, "#")
    #         stdscr.refresh()

    # for y in range(0, stdscr.getmaxyx()[0]):
    #     for x in range(0, stdscr.getmaxyx()[1]):
    #         stdscr.addstr(y, x, ".")
    #         stdscr.refresh()

    # for y in range(0, stdscr.getmaxyx()[0]):
    #     for x in range(0, stdscr.getmaxyx()[1]):
    #         stdscr.addstr(y, x, " ")
    #         stdscr.refresh()

    stdscr.addstr(9, 10, "A")
    stdscr.addstr(10, 9, "B")

    stdscr.addstr(19, 9, "C")  # 20, 9
    stdscr.addstr(20, 10, "D")  # 21, 10

    stdscr.addstr(20, 29, "E")  # 21, 30
    stdscr.addstr(19, 30, "F")  # 20, 31

    stdscr.addstr(10, 30, "G")  # 10, 31
    stdscr.addstr(9, 29, "H")  # 9,  30

    stdscr.addstr(9, 40,  "Win: 10x20 @ 10,10")
    stdscr.addstr(10, 42,   "#:  Wx h    x, y")
    stdscr.addstr(11, 42,   "A:          9,10")
    stdscr.addstr(12, 42,   "B:         10, 9")
    stdscr.addstr(13, 42,   "C:         19, 9")
    stdscr.addstr(14, 42,   "D:         20,10")
    stdscr.addstr(15, 42,   "E:         20,29")
    stdscr.addstr(16, 42,   "F:         19,30")
    stdscr.addstr(17, 42,   "G:         10,30")
    stdscr.addstr(18, 42,   "H:          9,29")

    stdscr.addstr(2, 3,   f'Window Size: {stdscr.getmaxyx()}')

    stdscr.box()

    win = curses.newwin(10, 20, 10, 10)
    win.box()

    win.addstr(1, 8, "Win")
    win.addstr(1, 1, "1")
    win.addstr(1, 18, "2")
    win.addstr(8, 18, "3")
    win.addstr(8, 1, "4")

    win.addstr(3, 6, "1: 1, 1")
    win.addstr(4, 6, "2: 1,18")
    win.addstr(5, 6, "3: 8,18")
    win.addstr(6, 6, "4: 8, 1")

    win.refresh()

    # for i in range(126, 1000):
    #     stdscr.addstr(0, 0, chr(i))
    #     # curses.cursor_pos = (
    #     #     curses.cursor_pos[0], curses.cursor_pos[1]+len(chr(i)))
    #     # stdscr.addstr(1, 0, str(i))
    #     # stdscr.addstr(2, 0, str(len(chr(i))))
    #     time.sleep(0.01)
    # curses.cursor_pos = (
    # curses.cursor_pos[0], curses.cursor_pos[1]+2)

    # stdscr.box()

    win2 = curses.newwin(5, 5, 20, 40)
    win2.box()

    # win2.addstr(0, 1, "ABC")
    win2.addstr(1, 1, "ABC")
    win2.addstr(2, 1, "ABC")
    win2.addstr(3, 1, "ABC")

    for y in range(0, stdscr.getmaxyx()[0]):
        for x in range(81, stdscr.getmaxyx()[1] - 2):
            stdscr.addstr(y, x, "#")
            stdscr.refresh()

    for y in range(0, stdscr.getmaxyx()[0], 1):
        stdscr.addstr(y, 3, str(y))
        stdscr.refresh()

    for x in range(0, stdscr.getmaxyx()[1], 1):
        stdscr.addstr(3, x, str(x % 10))
        stdscr.refresh()

    # win2.addstr(4, 1, "ABC")
    # win2.addstr(5, 0, "ABCDE")

    # val1 = time.monotonic_ns()
    # time.sleep(0.1)

    # val2 = time.monotonic_ns()

    # print("\n" + str((val2 - val1) / 1000))

    # TODO: it seems that the following two lines both draw at
    # the same location:

    # curses.write(escape.cup(0, 0) + "0")
    # curses.write(escape.cup(1, 1) + "1")
    # curses.write("\33[" + str(1) + ";" + str(103) + "H1")

    # curses.write("\33[" + str(2) + ";" + str(103) + "H@")
    # curses.write("\33[" + str(53) + ";" + str(103) + "H@")

    # curses.doupdate()
finally:
    # curses.echo()
    curses.curs_set(0)
    curses.endwin()

while not supervisor.runtime.serial_bytes_available:
    time.sleep(0.01)

sys.exit()


# curses = Curses()

# try:
#     curses.setup()

#     curses.beep()

#     curses.write("\33[0m")

#     curses.write("This is a test!")

#     # time.sleep(1)
#     curses.write("\33[7mthis is a test!")
#     # time.sleep(1)
#     curses.write("\33[0mSo is this!")

#     # curses.write("\033[500B")
#     # curses.write("\033[500C")

#     # curses.write("\33[7m")

#     curses.write("\033[500B")
#     curses.write("\033[3A")
#     curses.write("\033[500D")

#     sys.exit()

#     while True:
#         curses.update()
#         time.sleep(0.01)
# except OSError:
#     print("Error getting screen size: Timeout")

# sys.exit()
