# The MIT License (MIT)
#
# Copyright (c) 2020 Kevin Matocha
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
`kmatch98_textmap`
================================================================================

Text graphics handling for CircuitPython, including ttext boxes


* Author(s): Kevin Matocha

Implementation Notes
--------------------

**Hardware:**

.. todo:: Add links to any specific hardware product page(s), or category page(s). Use unordered list & hyperlink rST
   inline format: "* `Link Text <url>`_"

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

.. todo:: Uncomment or remove the Bus Device and/or the Register library dependencies based on the library's use of either.

# * Adafruit's Bus Device library: https://github.com/adafruit/Adafruit_CircuitPython_BusDevice
# * Adafruit's Register library: https://github.com/adafruit/Adafruit_CircuitPython_Register
"""

# imports

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/kmatch98/CircuitPython_textMap.git"

def lineSpacingY(font, lineSpacing, scale=1):
    # Note: Scale is not implemented at this time
    fontHeight = font.get_glyph(ord('M')).height
    returnValue = int(lineSpacing * fontHeight)
    return returnValue

def bounding_box(text, font, lineSpacing, scale=1):
    # bounding_box - determines the bounding box size around the new text to be added.
    #   To be used to calculate if the new text will be printed within the bounding_box
    #   This function can used to determine character-wrapping or word-wrapping for a
    #   text terminal box, prior to actually printing the text in the bitmap.
    #
    # Note: Scale is not implemented at this time
    boxHeight = boxWidth = 0
    fontHeight = font.get_glyph(ord("M")).height

    for char in text:
        myGlyph = font.get_glyph(ord(char))
        if myGlyph == None: # Error checking: no glyph found
            print('Glyph not found: {}'.format(repr(char)))
        else:
            width = myGlyph.width
            height = myGlyph.height
            dx = myGlyph.dx
            dy = myGlyph.dy
            shift_x = myGlyph.shift_x
            shift_y = myGlyph.shift_x

            # Not working yet***
            # This offset is used to match the label.py function from Adafruit_Display_Text library
            # y_offset = int(
            #     (
            #         self._font.get_glyph(ord("M")).height
            #         - new_text.count("\n") * self.height * self.line_spacing
            #     )
            #     / 2 )

            # yOffset = int( (fontHeight-height*lineSpacing)/2 )
            yOffset = fontHeight - height

            boxWidth = boxWidth + shift_x
            boxHeight = max(boxHeight, height - dy + yOffset)
    return (boxWidth, boxHeight)


def placeText(
    bitmap, text, font, lineSpacing, xPosition, yPosition, paletteIndex=1, scale=1
):
    # placeText - Writes text into a bitmap at the specified location.
    #
    # (xPosition, yPosition) correspond to upper left corner of the height of the 'M' glyph
    # To Do: Add anchor positions, and adjust the default baseline position to match
    #   the current "label" function
    # Verify paletteIndex is working properly with * operator, especially if accommodating multicolored fonts
    #
    # Note: Scale is not implemented at this time

    import terminalio

    fontHeight = font.get_glyph(ord("M")).height

    bitmapWidth = bitmap.width
    bitmapHeight = bitmap.height

    for char in text:

        myGlyph = font.get_glyph(ord(char))
        if myGlyph == None: # Error checking: no glyph found
            print('Glyph not found: {}'.format(repr(char)))
        else:

            width = myGlyph.width
            height = myGlyph.height
            # print('glyph width: {}, height: {}'.format(width, height))
            dx = myGlyph.dx
            dy = myGlyph.dy
            shift_x = myGlyph.shift_x
            shift_y = myGlyph.shift_x
            glyph_offset_x = myGlyph.tile_index * width # for type BuiltinFont, this creates the x-offset in the glyph bitmap.
                                                        # for BDF loaded fonts, this should equal 0

            # Not working yet***
            # This offset is used to match the label.py function from Adafruit_Display_Text library
            # y_offset = int(
            #     (
            #         self._font.get_glyph(ord("M")).height
            #         - new_text.count("\n") * self.height * self.line_spacing
            #     )
            #     / 2 )

            # position_y = y - glyph.height - glyph.dy + y_offset

            # yOffset = int( (fontHeight-height*lineSpacing)/2 )
            yOffset = fontHeight - height
            for y in range(height):
                for x in range(width):
                    xPlacement = x + xPosition + dx
                    # yPlacement=y+yPosition-height-dy+yOffset
                    yPlacement = y + yPosition - dy + yOffset

                    if (
                        (xPlacement >= 0)
                        and (yPlacement >= 0)
                        and (xPlacement < bitmapWidth)
                        and (yPlacement < bitmapHeight)
                    ):

                        # print('x: {}, y: {}, value: {}'.format(xPlacement, yPlacement, myGlyph.bitmap[x,y]))
                        bitmap[xPlacement, yPlacement] = (
                            myGlyph.bitmap[x+glyph_offset_x, y] * paletteIndex
                        )
            xPosition = xPosition + shift_x

    return (xPosition, yPosition)


class textBox:
    def __init__(
        self, text, font, width, height, backgroundColor=0x000000, textColor=0xFFFFFF, lineSpacing=1.25
    ):

        import displayio

        # import terminalio

        # To save memory, set self._memorySaver=True, avoids storing the text string in the class.
        # If set to False, the class saves the text string for future reference.
        self._memorySaver=True 

        if self._memorySaver == False:
            self._text = text  # text on the display
        self._font = font
        self._lineSpacing = lineSpacing
        self._fontHeight = self._font.get_glyph(ord("M")).height

        self._width = width  # in pixels
        self._height = height  # in pixels

        self._backgroundColor = backgroundColor
        self._textColor = textColor

        self.bitmap = displayio.Bitmap(self._width, self._height, 2)
        self.palette = displayio.Palette(2)
        if self._backgroundColor == None:
            self.palette.make_transparent(0)
        else:
            self.palette[0] = self._backgroundColor
        self.palette[1] = self._textColor

        self._cursorX = 1  # controls insertion point for text
        self._cursorY = 1

        self._startX = self._cursorX  # the left column start position
        self._startY = self._cursorY  # the top row start position

        self.addText(text)

        import gc

        gc.collect()

    def addText(self, newText):  # add text to a textBox
        # print('startX: {}'.format(self._cursorX) )
        import gc

        for char in newText:
            (charWidth, charHeight) = bounding_box(char, self._font, self._lineSpacing)
            if (self._cursorX + charWidth >= self._width - 1) or (char == "\n"):
                # make a newline
                self.setCursor(
                    self._startX,
                    self._cursorY + int(self._fontHeight * self._lineSpacing),
                )

            (newX, newY) = placeText(
                self.bitmap,
                char,
                self._font,
                self._lineSpacing,
                self._cursorX,
                self._cursorY,
            )
            # print('newX: {}'.format(newX) )
            self.setCursor(newX, newY)
            if self._memorySaver == False:
                self._text = self._text + newText # add this text to the instance text string.
        gc.collect()
        return self.getCursor()  # return tuple: (self._cursorX , self._cursorY)

    def setCursor(self, newCursorX, newCursorY):  # set cursor position
        self._cursorX = newCursorX
        self._cursorY = newCursorY

    def getCursor(self):  # get current cursor position, tuple
        return (self._cursorX, self._cursorY)

    def clearBitmap(self):
        self.bitmap.fill(0)
        self.setCursor(self._startX, self._startY)
        if self._memorySaver == False: 
            self._text='' # reset the text string
