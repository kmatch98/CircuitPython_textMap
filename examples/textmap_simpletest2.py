# Example that exercises the textMap library: https://github.com/kmatch98/CircuitPython_textMap
#

import board
import displayio
import terminalio
import busio

import textmap
from textmap import textBox

from adafruit_bitmap_font import bitmap_font

#from adafruit_st7789 import ST7789
from adafruit_ili9341 import ILI9341

displayio.release_displays()

spi = board.SPI()
tft_cs = board.D9 # arbitrary, pin not used
tft_dc = board.D10
tft_backlight = board.D12
tft_reset=board.D11

while not spi.try_lock():
    spi.configure(baudrate=32000000)
    pass
spi.unlock()

display_bus = displayio.FourWire(
    spi,
    command=tft_dc,
    chip_select=tft_cs,
    reset=tft_reset,
    baudrate=32000000,
    polarity=1,
    phase=1,
)

print('spi.frequency: {}'.format(spi.frequency))

DISPLAY_WIDTH=320
DISPLAY_HEIGHT=240

#display = ST7789(display_bus, width=DISPLAY_WIDTH, height=DISPlAY_HEIGHT, rotation=0, rowstart=80, colstart=0)
display = ILI9341(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, rotation=180, auto_refresh=True)

display.show(None)


myGroup = displayio.Group(max_size=10) # create a group to hold the text boxes

# Make a background color fill that covers the whole display
color_bitmap = displayio.Bitmap(DISPLAY_WIDTH, DISPLAY_HEIGHT, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x000000 # black

display_background = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
myGroup.append(display_background)
display.show(myGroup)

print('Showing background bitmap.')


print('loading fonts...')

font = terminalio.FONT # This is a fixed-width font of class "BuiltinFont"
fontText = bitmap_font.load_font('fonts/BitstreamVeraSans-Roman-24.bdf')
fontBold = bitmap_font.load_font('fonts/Helvetica-Bold-16.bdf')

print('Fonts are loaded.')

myText1 = textBox('This is a BuiltinFont with a\nnewline', font, 180, 40, backgroundColor=0x00FF00, textColor=0x000000)
myGroup.append(displayio.TileGrid(myText1.bitmap, pixel_shader=myText1.palette, x=30, y=5)) 

myText2 = textBox('BDF imported font', fontBold, 300, 40, backgroundColor=0xFF0000, textColor=0xFFFFFF)
myGroup.append(displayio.TileGrid(myText2.bitmap, pixel_shader=myText2.palette, x=5, y=60)) 

myText3 = textBox('Another BDF imported font', fontText, 280, 60, backgroundColor=0x0000FF, textColor=0xFFFFFF)
myGroup.append(displayio.TileGrid(myText3.bitmap, pixel_shader=myText3.palette, x=20, y=120))

myText4 = textBox('BuiltinFont hard wrapped text in this box, transparent background', font, 120, 100, backgroundColor=None, textColor=0x44FF44, lineSpacing=1.0)
myGroup.append(displayio.TileGrid(myText4.bitmap, pixel_shader=myText4.palette, x=80, y=150))

myText5 = textBox('BuiltinFont\ntextBox\ntransparent\nbackground', font, 120, 100, backgroundColor=None, textColor=0xFF00FF, lineSpacing=1.0)
myGroup.append(displayio.TileGrid(myText5.bitmap, pixel_shader=myText5.palette, x=230, y=150))

print('Printed text.')

import time
time.sleep(100000) # delay for a long while
