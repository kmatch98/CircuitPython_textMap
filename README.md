

# What it does
Memory-conserving text graphics handling for CircuitPython, including colored text boxes.

![Demo of textmap_simpletest.py](examples/textmap_simpletest.gif)

# Usage

    import textmap
    from textmap import textBox

This set of text display routines attempts to overcome the large memory usage of the current "label" function in the CircuitPython Display_Text library.  That function uses a collection of tileGrid (one per character) to handle printing proportional fonts.  The tileGrid approach comes with a lot of overhead that may be useful or unnecessary depending upon your application.
https://github.com/adafruit/Adafruit_CircuitPython_Display_Text

This `textmap` library attempts to reduce memory usage by letting you provide a bitmap where the text is written.

This library consists of two generic functions for writing text to the screen and then an example class `textBox` with capabilities for handling cursor position and inserting text.

### Key Basic Functions
- `placeText` - Add the text to a bitmap
- `bounding_box` - If I want to print some text, how large of a box is required to fit it?


Example Class `textBox` - Creates a bitmap and handles cursor position, adding text and clearing the box. The functions handle word wrapping.

### Class Functions: `textBox` 
- `addText` - Add some text to the box at the current cursor position
- `setCursor` - Change the cursor (x,y) position
- `getCursor` - Returns the cursor (x,y) position
- `clearBitmap` - Clears the textBox bitmap to the original background color


# Key Basic Functions
The `placeText` function transfers text into a bitmap at the specified x and y locations.  For this function, you provide a `bitmap`, the `text`, `font` and `lineSpacing` and `x` and `y` locations for text to be added.  This functions writes the text into your bitmap.

The `bounding_box` function is used to determine how large of a box (x and y) is required to cover the prospective text that you want to write.  This function is useful to calculate if a proposed text string will fit where you want to put it.  That way, you can determine if the text will fit before you write it.  This is particularly useful for word-wrapping or text-wrapping in a text terminal window.

Note: Currently, the builtinFont `terminalio.FONT` is not handled with these functions.  (Reason: The terminalio.FONT builtinFont class is a fixed-sized font and its class is defined a little bit differently than an imported BDF font.)

# Example Class: textBox

The `textBox` example class provides a few structures and methods for creating and handling text addition into a rectangular box.  The `textBox` consists of a bitmap (`length`, `width`, `backGroundColor`), along with the required parameters to define the text that is to be added 
(`font`, `textColor`, `lineSpacing`).

The `textBox` class includes several functions for adding text (`addText`), setting and getting the cursor position (`setCursor` and `getCursor`) and clearing the bitmap (`clearBitMap`).

Once you instance a `textBox`, you can then add the `textBoxName.bitmap` into a tileGrid for further displaying on an attached display.

# Simple Example Usage: `textmap_simpletest.py`

The example file `textmap_simpletest.py` creates four textBox instances and plots them to the screen. This example uses the three fonts located in the `fonts` subdirectory.

Each time through the while loop, one character is added to the `textBox`.  Whenever the full string has been written, the `textBox` is cleared and text writing begins again.  One of the boxes is stationary, while the other three are then moved around on the screen.  


Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_.

Installing from PyPI
=====================
.. note:: This library is not available on PyPI yet. Install documentation is included
   as a standard element. Stay tuned for PyPI availability!

.. todo:: Remove the above note if PyPI version is/will be available at time of release.
   If the library is not planned for PyPI, remove the entire 'Installing from PyPI' section.

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-textmap/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-textmap

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-textmap

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-textmap

Usage Example
=============

.. todo:: Add a quick, simple example. It and other examples should live in the examples folder and be included in docs/examples.rst.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/kmatch98/Kmatch98_CircuitPython_textMap/blob/master/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
