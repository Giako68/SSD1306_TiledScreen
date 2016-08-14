#
# TiledScreen Demo
#
 
from TiledScreen import TiledScreen
from uos import urandom
from utime import sleep_ms

def Start():
    TS = TiledScreen("Font.dat")
    for y in range(8):
        for x in range(16):
            TS.SetTile(x, y, 32)
    while(True):
         N = (urandom(1)[0] % 5) + 1
         Size = (urandom(1)[0] % 4) + 1
         start = 4 - Size
         for i in range(N):
             data = urandom(Size * 2)
             TS.HorizontalScroll(start, True, data)
         N = (urandom(1)[0] % 5) + 1
         Size = (urandom(1)[0] % 8) + 1
         start = 8 - Size
         for i in range(N):
             data = urandom(Size * 2)
             TS.VerticalScroll(start, True, data)
         N = (urandom(1)[0] % 5) + 1
         Size = (urandom(1)[0] % 4) + 1
         start = 4 - Size
         for i in range(N):
             data = urandom(Size * 2)
             TS.HorizontalScroll(start, False, data)
         N = (urandom(1)[0] % 5) + 1
         Size = (urandom(1)[0] % 8) + 1
         start = 8 - Size
         for i in range(N):
             data = urandom(Size * 2)
             TS.VerticalScroll(start, False, data)
         
