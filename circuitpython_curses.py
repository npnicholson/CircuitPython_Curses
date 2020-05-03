# The MIT License (MIT)
#
# Copyright (c) 2020 Norris Nicholson for Entalon LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`circuitpython_curses`
================================================================================

Lightweight CircuitPython Curses implementation for the usb serial interface


* Author(s): Norris Nicholson

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered
   list & hyperlink rST inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

"""

# imports
__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/npnicholson/Circuitpython_Curses.git"

import sys
import time
import supervisor


# For compatability with the curses codebase, ignore this pylint error
# pylint: disable=invalid-name
class curses:
    """CircuitPython Curses Implementation.
    """

    # For compatability with the curses codebase, ignore this pylint error
    # pylint: disable=invalid-name
    class error(Exception):
        """ Exception raised when a curses library function returns an error.
        """

    cursor_pos = (0, 0)

    def __init__(self):
        pass

    @staticmethod
    def initscr():
        """ Initialize the library. Return a window object which represents the whole screen.
        """

        # Clear the entire screen
        curses.write("\033[2J")
        curses.write("\33[0m")

        # Move the cursor to 500, 500
        curses.write("\033[500B")
        curses.write("\033[500C")

        # Ask the term where the cursor is
        curses.write("\033[6n")

        # Clear the screen again
        curses.write("\033[2J")

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
                if char is escape.RSP:
                    done = True
                    break

            # Wait for more serial data
            time.sleep(0.01)

            # If we have been waiting too long, fail
            if counter > 100:
                raise OSError("Unable to get screen size: Timeout")

        escape_arguments = escape(buf).get_args()

        # Window size is reduced by 4 because the window cannot extend all the way to
        # the right side without causing distortions on UNICODE characters (which have a
        # visible length of 1, but a codeunit length of 2):
        # https://stackoverflow.com/questions/30775689/python-length-of-unicode-string-confusion
        return curses.newwin(
            int(escape_arguments[0]), int(escape_arguments[1]) - 4, 0, 0
        )

    @staticmethod
    def endwin():
        """ De-initialize the library, and return terminal to normal status. - Stub - not used for
            circuit python implementation
        """

    @staticmethod
    def newwin(nlines, ncols, begin_y=0, begin_x=0):
        """ Return a new window, whose left-upper corner is at (begin_y, begin_x),
            and whose height/width is nlines/ncols.
        """
        # Offset by two pixels to account for the fact that the top level window
        # has an x_pos of 2
        return window((nlines - 1, ncols), begin_y, begin_x + 1)

    @staticmethod
    def write(text):
        """ Prints to the console without a newline
        """
        print(text, end="")

    @staticmethod
    def write_pos(y, x, string):
        """ Prints to the console without a newline at the specified location
        """

        # Calculate the current offset between where the cursor is, and where
        # we want it to be
        y_offset = y - curses.cursor_pos[0]
        x_offset = x - curses.cursor_pos[1]

        # Add the approperate strings to the buffer as needed to move
        # the cursor to where it needs to be
        if y_offset > 0:
            curses.write(escape.cud(y_offset))
        elif y_offset < 0:
            curses.write(escape.cuu(-y_offset))
        if x_offset > 0:
            curses.write(escape.cuf(x_offset))
        elif x_offset < 0:
            curses.write(escape.cub(-x_offset))

        # Write the buffer string plus the desired string to the
        # console
        curses.write(string)

        # Adjust the cursor position based on the length of the string
        # we just wrote. We encode the string so that we catch any unicode
        # characters in the string and adjust as needed. This is only
        # needed to measure the visual length of the string on the screen.
        # Calling .encode() on a string with escape sequences will remove
        # the sequences
        curses.cursor_pos = (y, x + len(string.encode()))

        # Add one to the y offset for the cup method
        # curses.write("\33[" + str(y + 1) + ";" + str(x) + "H" + string)

        # curses.write("\033[0;0H\033[" + str(y) +
        #              "B\033[" + str(x) + "C" + string)

    @staticmethod
    def beep():
        """ Emit a short attention sound.
        """
        curses.write("\07")

    @staticmethod
    def curs_set(setting):
        """ Set the cursor state. visibility can be set to 0, 1, for invisible, normal.
        """
        if setting == 0:
            curses.write("\33[?25l")
        elif setting == 1:
            curses.write("\33[?25h")
        elif setting == 2:
            raise AttributeError("curs_set (2) [very visible] not implemented")
        else:
            raise AttributeError("curs_set argument must be 0 or 1: " + setting)

    @staticmethod
    def delay_output(milliseconds):
        """ Insert an ms millisecond pause in output.
        """
        time.sleep(milliseconds / 1000)

    @staticmethod
    def flushinp():
        """ Flush all input buffers.
        """
        # TODO: There has to be a better way to clear the usb serial buffer
        while supervisor.runtime.serial_bytes_available:
            sys.stdin.read(1)


# For compatability with the curses codebase, ignore this pylint error
# pylint: disable=invalid-name
class window:
    """ Window objects, as returned by initscr() and newwin()
    """

    def __init__(self, window_size=(0, 0), y_pos=0, x_pos=0):
        self.window_size = window_size
        self.x_pos = x_pos
        self.y_pos = y_pos

    def addstr(self, y, x, string):
        """ Paint the character string str at (y, x) with attributes attr, overwriting anything
            previously on the display.
        """
        if not self._in_bounds(y, x, string):
            raise curses.error(f"Out of Bounds: ({y},{x}) {self.window_size}")

        curses.write_pos(y + self.y_pos, x + self.x_pos, string)

    def box(self):
        """ Draw a box around the edges of the window.
        """
        self.addstr(0, 0, "┌")
        for x in range(1, self.window_size[1]):
            self.addstr(0, x, "─")

        self.addstr(0, self.window_size[1] - 1, "┐")
        for y in range(1, self.window_size[0]):
            self.addstr(y, self.window_size[1] - 1, "│")

        self.addstr(self.window_size[0], self.window_size[1] - 1, "┘")

        for x in range(self.window_size[1] - 2, 0, -1):
            self.addstr(self.window_size[0], x, "─")

        self.addstr(self.window_size[0], 0, "└")

        for y in range(self.window_size[0] - 1, 0, -1):
            self.addstr(y, 0, "│")

    def _in_bounds(self, y, x, string):
        if (
            y > self.window_size[0]
            or y < 0
            or x + len(string) > self.window_size[1]
            or x < 0
        ):
            return False

        return True

    def refresh(self):
        """ Update the display immediately. Stub - not used for circuit python implementation
        """

    def getmaxyx(self):
        """ Return a tuple (y, x) of the height and width of the window.
        """
        return (self.window_size[0] + 1, self.window_size[1])

    # For compatability with the curses codebase, ignore this pylint error
    # pylint: disable=no-self-use
    def getch(self):
        """ Get a character. Note that the integer returned does not have to be in ASCII range:
            function keys, keypad keys and so on are represented by numbers higher than 255.
            In no-delay mode, return -1 if there is no input, otherwise wait until a key is pressed.
        """
        if supervisor.runtime.serial_bytes_available:
            return sys.stdin.read(1)

        return -1


# For compatability with the curses codebase, ignore this pylint error
# pylint: disable=invalid-name


class escape:
    """ Class for managing ansi escape sequences
    """

    ESC = "\33"
    CSI = "\33["
    RET = "\27["

    # Shorts
    RSP = "R"  # Response from the Terminal

    # Full Codes
    DECTCE_SHOW = "\27[?25h"  # Shows the Cursor
    DECTCE_HIDE = "\27[?25l"  # Hides the Cursor

    def __init__(self, inpt):
        self.code = inpt

    def get_command(self):
        """ Returns the command code for the escape, which is the last charactor
        """
        return self.code[-1]

    def get_body(self):
        """ Returns the body of the excape, which is the content between '[' and the last
            character
        """
        return self.code[self.code.find("[") + 1 : len(self.code) - 1]

    def get_args(self):
        """ Returns the arguments of the escape, as split by ';'
        """
        return self.get_body().split(";")

    # @property
    @staticmethod
    def cuu(n):
        """ Escape to move the cursor up by n lines
        """
        return f"\33[{n}A"

    @staticmethod
    def cud(n):
        """ Escape to move the cursor down by n lines
        """
        return f"\33[{n}B"

    @staticmethod
    def cuf(n):
        """ Escape to move the cursor forward by n lines
        """
        return f"\33[{n}C"

    @staticmethod
    def cub(n):
        """ Escape to move the cursor back by n lines
        """
        return f"\33[{n}D"

    @staticmethod
    def ed(n=""):
        """ Escape to clear the display: CSI n J
        """
        return f"\33[{n}J"

    @staticmethod
    def cup(y, x):
        """ Escape to move the cursor to the specified position
        """

        # Add one to y to account for the fact that cup 0, 0 and cup 1, 1
        # both place at the top of the screen. In order to make the top corner
        # 0, we add one to both values
        return f"\33[{y+1};{x+1}H"
