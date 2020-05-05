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

    COLOR_BLACK = 0
    COLOR_BLUE = 4
    COLOR_CYAN = 6
    COLOR_GREEN = 2
    COLOR_MAGENTA = 5
    COLOR_RED = 1
    COLOR_WHITE = 15
    COLOR_YELLOW = 11
    COLOR_NONE = -1

    MODE_16 = 0
    MODE_256 = 1

    # TODO: Procedurally generate this instead to save memory if we don't need it?
    _COLOR_256_16_FG = {
        0: 30,
        1: 31,
        2: 32,
        3: 33,
        4: 34,
        5: 35,
        6: 36,
        7: 37,
        8: 90,
        9: 91,
        10: 92,
        11: 93,
        12: 94,
        13: 95,
        14: 96,
        15: 97,
    }

    # TODO: Procedurally generate this instead to save memory if we don't need it?
    _COLOR_256_16_BG = {
        0: 40,
        1: 41,
        2: 42,
        3: 43,
        4: 44,
        5: 45,
        6: 46,
        7: 47,
        8: 100,
        9: 101,
        10: 102,
        11: 103,
        12: 104,
        13: 105,
        14: 106,
        15: 107,
    }

    background = 0x3FE00
    foreground = 0x1FF

    # 0 = 16 colors
    # 1 = 256 colors
    color_mode = MODE_256

    _color_pairs = {}

    _cursor_pos = (0, 0)

    _use_string_encoding = False

    def __init__(self):
        pass

    @staticmethod
    def initscr():
        """ Initialize the library. Return a window object which represents the whole screen.
        """

        # TODO: Find out which terminal we are on and what it supports:
        # minicom: _use_sring_encoding = True
        #          only 16 base colors: ESC[30;47m
        # Screen:  _use_string_encoding = False
        #          all colors

        # Request the terminal askback
        curses.write("\005")
        time.sleep(0.1)

        # See if we get a response. Some terminals will not return anything
        if supervisor.runtime.serial_bytes_available:
            # Read in one character
            char = sys.stdin.read(1)

            # If the character is M, then we might be on minicom
            if char is "M":
                curses._use_string_encoding = True
                # color_mode = 0

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

        # Move the cursor to 0, 0
        curses.write("\33[;H")

        curses._cursor_pos = (0, 0)

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
    def color_pair(color_number):
        """ Return the attribute value for displaying text in the specified color. This attribute
            value can be combined with A_STANDOUT, A_REVERSE, and the other A_* attributes.
        """
        try:
            return curses._color_pairs[color_number]
        except KeyError:
            return 0

    @staticmethod
    def init_pair(pair_number, fg, bg):
        """ Change the definition of a color-pair. It takes three arguments: the number of the
            color-pair to be changed, the foreground color number, and the background color number.
            The value of pair_number must be between 1 and COLOR_PAIRS - 1 (the 0 color pair is
            wired to white on black and cannot be changed). The value of fg and bg arguments must
            be between 0 and COLORS. If the color-pair was previously initialized, the screen is
            refreshed and all occurrences of that color-pair are changed to the new definition.
        """

        # Encode negative values as 256 for the background and foreground
        if fg < 0:
            fg = 256

        if bg < 0:
            bg = 256

        # 01234567 012345678 012345678
        # other    bckgnd    frgnd
        curses._color_pairs[pair_number] = bg << 9 | fg

    @staticmethod
    def start_color():
        """ start_color() initializes eight basic colors (black, red, green, yellow, blue, magenta,
            cyan, and white), and two global variables in the curses module, COLORS and COLOR_PAIRS,
            containing the maximum number of colors and color-pairs the terminal can support.

            Stub - not used for circuitpython implementation
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
    def write_pos(y, x, string, prefix, postfix):
        """ Prints to the console without a newline at the specified location
        """

        # Calculate the current offset between where the cursor is, and where
        # we want it to be
        y_offset = y - curses._cursor_pos[0]
        x_offset = x - curses._cursor_pos[1]

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

        # If there is a prefix to write, do so first
        if prefix:
            curses.write(prefix)

        # Then write the string
        curses.write(string)

        # Then write any postfix
        if postfix:
            curses.write(postfix)

        # Adjust the cursor position based on the length of the string
        # we just wrote. We encode the string so that we catch any unicode
        # characters in the string and adjust as needed. This is only
        # needed to measure the visual length of the string on the screen.
        #
        # We only measure the proper string for moving the cursor. All escapes should be
        # placed in the prefix and postfix
        if curses._use_string_encoding:
            curses._cursor_pos = (y, x + len(string.encode()))
        else:
            curses._cursor_pos = (y, x + len(string))

        # Add one to the y offset for the cup method
        # curses.write("\33[" + str(y + 1) + ";" + str(x) + "H" + string)

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

    @staticmethod
    def _get_fg(attr):
        """ Decodes the attr var to get the foreground color
        """
        _cl = attr & curses.foreground
        return None if _cl is 256 else _cl

    @staticmethod
    def _get_bg(attr):
        """ Decodes the attr var to get the background color
        """
        _cl = (attr & curses.background) >> 9
        return None if _cl is 256 else _cl

    @staticmethod
    # TODO: May not need this method anymore
    def clean_ansi(string):
        """ Cleans a color ansi code out of a string
        """
        # Get the location of the first escape sequence. If non exists, this will return a -1 and
        # the loop will be skipped
        _l = string.find("\33[")
        # While there is another escape sequence to remove, loop
        while _l is not -1:
            # Cut the sequence out of the string. Starting at the escape sequence, look for
            # the letter "m", which denotes the end of the sequence. Set the string to be that
            # portion of the string which is before and after the escape.
            string = string[:_l] + string[string.find("m", _l) + 1 :]

            # Find the next escape sequence, if there is one. If non exists, this will return a -1
            # and the loop will end
            _l = string.find("\33[")

        # Return the modified string
        return string


# For compatability with the curses codebase, ignore this pylint error
# pylint: disable=invalid-name
class window:
    """ Window objects, as returned by initscr() and newwin()
    """

    def __init__(self, window_size=(0, 0), y_pos=0, x_pos=0):
        self.window_size = window_size
        self.x_pos = x_pos
        self.y_pos = y_pos

    def addnstr(self, y, x, n, string, attr=None):
        """ Paint at most n characters of the character string str at (y, x) with attributes attr,
            overwriting anything previously on the display.
        """
        return self.addstr(y, x, string[0:n], attr)

    def addstr(self, y, x, string, attr=None):
        """ Paint the character string str at (y, x) with attributes attr, overwriting anything
            previously on the display.
        """

        # TODO: Add support for A_ attributes (like blink, underline, etc)

        # Set prefix and postfix to None here incase they are not set to something else later
        prefix = None
        postfix = None

        # See if there is an attribute
        if attr:
            # pylint: disable=protected-access
            fg = curses._get_fg(attr)
            bg = curses._get_bg(attr)

            # 16 color mode
            if curses.color_mode is curses.MODE_16:

                # TODO: Add support for intensity (currently set at 1)
                # We are using 16 colors
                if fg or bg:
                    postfix = "\33[m"
                    # Try to translate the color from 256 to 16. If there is a key error, then there
                    # is not a translation between the color modes. In that case, we write nothing
                    # to prefix
                    try:
                        if fg:
                            fg = curses._COLOR_256_16_FG[fg]
                    except KeyError:
                        fg = curses._COLOR_256_16_FG[curses.COLOR_BLACK]
                    try:
                        if bg:
                            bg = curses._COLOR_256_16_BG[bg]
                    except KeyError:
                        bg = curses._COLOR_256_16_BG[curses.COLOR_BLACK]

                    if fg and bg:
                        prefix = "\33[1;" + str(fg) + ";1;" + str(bg) + "m"
                    else:
                        # If fg and bg arent set, then only one of them is. Use which ever setting
                        # only
                        prefix = "\33[1;" + str(fg or bg) + "m"

            # 256 color mode
            else:
                if fg or bg:
                    postfix = "\33[m"
                    if fg and bg:
                        prefix = "\33[38;5;" + str(fg) + ";48;5;" + str(bg) + "m"
                    elif fg:
                        prefix = "\33[38;5;" + str(fg) + "m"
                    else:  # bg
                        prefix = "\33[48;5;" + str(bg) + "m"

        # TODO: Wrapping does not seem to work with special characters (eg: ▆)

        # Split the input string by newline characters and grab each split string as an individual.
        # If there are no newline characters in the string, the for loop will run only once
        lst = string.split("\n")
        lst_len = len(lst) - 1  # This line minus one to reduce work in the loop
        for idx, line in enumerate(lst):

            # While this split string is longer than the window, starting at the given x position,
            # cut it into smaller strings and simulate a newline
            while x + len(line.encode()) > self.window_size[1]:

                # Cut the string so that it will fit in this line
                self._addstr(y, x, line[0 : self.window_size[1] - x], prefix=prefix)

                # Set the prefix to an empty string because we have already written it to the
                # screen
                prefix = ""

                # Move to the next line, and set the cursor to the start of the window
                y = y + 1
                x = 0

                # Use the remainder of the cut string above for next time loop
                line = line[self.window_size[1] - x :]

            # After the string has been cut until it can fit in a single line, print the string. If
            # the string was never bigger than a single line, then only this _addstr will run. If
            # we are not at the end of our for loop, then we have arrived at a newline character.
            # In this case, print the line plus padded spaces to the end of the line. This is to
            # replicate curses
            if idx < lst_len:
                self._addstr(
                    y,
                    x,
                    line + " " * (self.window_size[1] - len(line.encode())),
                    prefix=prefix,
                )

                # Set the prefix to an empty string because we have already written it to the
                # screen
                prefix = ""
                # Now we have reached the end of the first split string. If there are more strings
                # split based on newline characters, then we want to prep for them next loop. Go
                # ahead and move to the next line, and set the x position to 0
                y = y + 1
                x = 0
            else:
                # Since this will always be run at least once, at the very end of the string, we
                # add the postfix here
                self._addstr(y, x, line, prefix=prefix, postfix=postfix)

                # Don't need to worry about clearing prefix or postfix here because this is the
                # end of the loop

    def _addstr(self, y, x, string, prefix=None, postfix=None):
        """ Internal function for writing to the screen. Checks to ensure that the given string
            will not exceed the boundries of the window.

            Also checks to ensure that the last character in the window is not written to. This 
            seems to be a quirk with curses that needs to be emulated.
        """

        str_len = len(string.encode())

        # Ensure that we have not written up to the last character in the window. This is
        # a quirk with curses that needs to be replicated
        if (
            # Ensure that y is not greater than the window size
            y > self.window_size[0]
            # Ensure that y is not negative
            or y < 0
            # Ensure that x plus whatever we are writing to the screen is less than or equal to
            # the width of the window
            or x + str_len > self.window_size[1]
            # Ensure that x is not negative
            or x < 0
        ):
            raise curses.error(
                "A Out of Bounds: ("
                + str(y)
                + ","
                + str(x)
                + ") "
                + str(self.window_size)
            )

        # Make sure that the last character in the window will not be written to
        if y >= self.window_size[0] and x + str_len >= self.window_size[1]:
            raise curses.error("Can't write to the last cell in a window")

        # Write the string to the screen
        self._write_pos(y, x, string, prefix=prefix, postfix=postfix)

    def _write_pos(self, y, x, string, prefix=None, postfix=None):
        """ Internal function for executing the curses.write_pos command, with the correct
            offset based on this window's position.

            This function does no verification of the location of the draw. Therefore, it is
            possible with this function to draw outside the bounds of the window
        """
        curses.write_pos(
            y + self.y_pos, x + self.x_pos, string, prefix=prefix, postfix=postfix
        )

    def box(self):
        """ Draw a box around the edges of the window.
        """
        self._write_pos(0, 0, "┌")  # ┌╭
        for x in range(1, self.window_size[1]):
            self._write_pos(0, x, "─")

        self._write_pos(0, self.window_size[1] - 1, "┐")  # ┐╮
        for y in range(1, self.window_size[0]):
            self._write_pos(y, self.window_size[1] - 1, "│")

        self._write_pos(self.window_size[0], self.window_size[1] - 1, "┘")  # ┘╯

        for x in range(self.window_size[1] - 2, 0, -1):
            self._write_pos(self.window_size[0], x, "─")

        self._write_pos(self.window_size[0], 0, "└")  # └╰

        for y in range(self.window_size[0] - 1, 0, -1):
            self._write_pos(y, 0, "│")

    def refresh(self):
        """ Update the display immediately. Stub - not used for circuit python implementation
        """

    def getmaxyx(self):
        """ Return a tuple (y, x) of the height and width of the window.
        """
        return (self.window_size[0] + 1, self.window_size[1])

    def getbegyx(self):
        """ Return a tuple (y, x) of co-ordinates of upper-left corner.
        """
        return (self.y_pos, self.x_pos - 1)

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
        # return f"\33[{n}A"
        return "\33[" + str(n) + "A"

    @staticmethod
    def cud(n):
        """ Escape to move the cursor down by n lines
        """
        # return f"\33[{n}B"
        return "\33[" + str(n) + "B"

    @staticmethod
    def cuf(n):
        """ Escape to move the cursor forward by n lines
        """
        # return f"\33[{n}C"
        return "\33[" + str(n) + "C"

    @staticmethod
    def cub(n):
        """ Escape to move the cursor back by n lines
        """
        # return f"\33[{n}D"
        return "\33[" + str(n) + "D"

    @staticmethod
    def ed(n=""):
        """ Escape to clear the display: CSI n J
        """
        # return f"\33[{n}J"
        return "\33[" + str(n) + "J"

    @staticmethod
    def cup(y, x):
        """ Escape to move the cursor to the specified position
        """

        # Add one to y to account for the fact that cup 0, 0 and cup 1, 1
        # both place at the top of the screen. In order to make the top corner
        # 0, we add one to both values
        # return f"\33[{y+1};{x+1}H"
        return "\33[" + str(y + 1) + ";" + str(x + 1) + "H"
