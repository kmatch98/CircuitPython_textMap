# Sample code using the textMap library and the "textBox" wrapper class
# Creates four textBox instances
# Inserts each textBox into a tileGrid group
# Writes text into the box one character at a time
# Moves the position of the textBox around the display
# Clears each textBox after the full string is written (even if the text is outside of the box)

import textmap
from textmap import textBox

import board
import displayio
import time
import terminalio
import fontio
import sys
import busio
#from adafruit_st7789 import ST7789
from adafruit_ili9341 import ILI9341

#  Setup the SPI display

print('Starting the display...') # goes to serial only
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

#display = ST7789(display_bus, width=240, height=240, rotation=0, rowstart=80, colstart=0)
display = ILI9341(display_bus, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, rotation=180, auto_refresh=True)

display.show(None)

print ('Display is started')


# load all the fonts
print('loading fonts...')

import terminalio


fontList = []
fontHeight = []

##### the BuiltinFont terminalio.FONT has a different return strategy for get_glyphs and 
# is currently not handled by these functions.
#fontList.append(terminalio.FONT)
#fontHeight = [10] # somehow the terminalio.FONT needs to be adjusted to 10

# Load some proportional fonts
fontFiles =   [
            'fonts/Helvetica-Bold-16.bdf',
            'fonts/BitstreamVeraSans-Roman-24.bdf', # Header2
            'fonts/BitstreamVeraSans-Roman-16.bdf', # mainText
            ]

from adafruit_bitmap_font import bitmap_font

for i, fontFile in enumerate(fontFiles):
    thisFont = bitmap_font.load_font(fontFile) 
    fontList.append(thisFont)
    fontHeight.append( thisFont.get_glyph(ord("M")).height ) 

preloadTheGlyphs= True # set this to True if you want to preload the font glyphs into memory
    # preloading the glyphs will help speed up the rendering of text but will use more RAM

if preloadTheGlyphs:

    # identify the glyphs to load into memory -> increases rendering speed
    glyphs = b'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-,.:?! '

    print('loading glyphs...')
    for font in fontList:
        font.load_glyphs(glyphs)
    print('Glyphs are loaded.')

print('Fonts completed loading.')

# create group 
import gc
gc.collect()
print( 'Memory free: {}'.format(gc.mem_free()) )

textBoxes=[] # list of textBox instances

textBoxes.append( textBox('', DISPLAY_WIDTH, DISPLAY_HEIGHT, 0x000000, 0x443344, fontList[0]) )
print( 'Memory free: {}'.format(gc.mem_free()) )
textBoxes.append( textBox('', 150, 60, 0x000000, 0xFFFFFF, fontList[0]) )
print( 'Memory free: {}'.format(gc.mem_free()) )
textBoxes.append( textBox('', 160, 100, 0xFF00FF, 0xFFFFFF, fontList[1]) )
print( 'Memory free: {}'.format(gc.mem_free()) )
textBoxes.append( textBox('', 180, 80, 0x00FFFF, 0x444444, fontList[2]) )
print( 'Memory free: {}'.format(gc.mem_free()) )
gc.collect()
myGroup = displayio.Group( max_size=len(textBoxes) ) # Create a group for displaying

tileGridList=[] # list of tileGrids


#startPositions
x=[0, 10, 160, 50]
y=[0, 20, 80, 150]

xVelocity=[0,  1, -1, 2]
yVelocity=[0, -1,  2, 1]

gc.collect()
stringList=[]
stringList.append('Full Screen Size: This is a stationary box, not a stationery box. Full Screen Size: This is a stationary box, not a stationery box. Full Screen Size: This is a stationary box, not a stationery box. Full Screen Size: This is a stationary box, not a stationery box. Full Screen Size: This is a stationary box, not a stationery box. Full Screen Size: This is a stationary box, not a stationery box. Full Screen Size: This is a stationary box, not a stationery box. Full Screen Size: This is a stationary box, not a stationery box. Full Screen Size: This is a stationary box, not a stationery box. Full Screen Size: This is a stationary box, not a stationery box.')
stringList.append('Helvetica Bold 16 font - with Black background color')
stringList.append('Vera Sans 24 font - this is a longer line that is wrapping around')
stringList.append('Vera Sans 16 font - how much text will this hold but it will not print text that goes outside the box but it will cut it off at the bottom if it is too large.')

for i, box in enumerate(textBoxes):
    tileGridList.append (displayio.TileGrid(box.bitmap, pixel_shader=box.palette, x=x[i], y=y[i]) )
    myGroup.append(tileGridList[i])
display.show(myGroup)

charCount=0
while True:

    # Add characters one at a time.

    for i, box in enumerate(textBoxes):
        charToPrint=charCount % len(stringList[i])
        if charToPrint == 0:
            box.clearBitmap()
        box.addText(stringList[i][charToPrint]) # add a character
        gc.collect()
    
    charCount += 1

    # Move each box 

    for i, thisTileGrid in enumerate(tileGridList):
        targetX=thisTileGrid.x + xVelocity[i]
        targetY=thisTileGrid.y + yVelocity[i]
        if ( (targetX + textBoxes[i].bitmap.width) >= DISPLAY_WIDTH ) or (targetX < 0):
            xVelocity[i] = -1* xVelocity[i]
        if ( (targetY + textBoxes[i].bitmap.height) >= DISPLAY_HEIGHT ) or (targetY < 0):
            yVelocity[i] = -1* yVelocity[i]
        thisTileGrid.x=thisTileGrid.x + xVelocity[i]
        thisTileGrid.y=thisTileGrid.y + yVelocity[i]
        gc.collect()

    # Print the memory availability every 10 movements.
    if charCount % 10 == 0:
        print( 'Memory free: {}'.format(gc.mem_free()) )







