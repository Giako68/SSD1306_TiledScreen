#
# Tiled Screen using SSD1306 display controller
#
# Tile size: 8x8 pixel
#

from SSD1306 import SSD1306

class TiledScreen(object):
      def __init__(self, tiles, display=None):
          if (display == None):
             self.Display = SSD1306(scl=4, sda=5, addr=60)
          else:
             self.Display = display
          F = open(tiles, "rb")
          self.Tiles = F.read(2048)
          F.close()
          self.TileMap = [0 for i in range(128)]
          self.Display.SetHorizontalAddressingMode()
          self.Refresh()
          
      def Refresh(self):
          self.Display.SetWriteWindow(0, 7, 0, 127)
          for i in self.TileMap:
              self.Display.SendData(self.Tiles[i*8:i*8+8])
              
      def Clear(self, tile=0):
          for i in range(128):
              self.TileMap[i] = tile
          self.Refresh()

      def SetTile(self, x, y, t):
          self.TileMap[y*16+x] = t
          self.Display.SetWriteWindow(y, y, x*8, x*8+7)
          self.Display.SendData(self.Tiles[t*8:t*8+8])
          
      def HorizontalScroll(self, start, direction, data):
          if (start < 0) or (start > 7):
             return
          if (start + len(data) > 8):
             return
          for y in range(start, start+len(data)):
              for x in range(15):
                  if direction:
                     self.TileMap[y*16+x] = self.TileMap[y*16+x+1]
                  else:
                     self.TileMap[y*16+(15-x)] = self.TileMap[y*16+(15-x-1)]
              if direction:
                 self.TileMap[y*16+15] = data[y-start]
              else:
                 self.TileMap[y*16] = data[y-start]
          self.Display.SetWriteWindow(start, start+len(data)-1, 0, 127)
          for n in range(start*16, (start + len(data))*16):
              i = self.TileMap[n]
              self.Display.SendData(self.Tiles[i*8:i*8+8])

      def VerticalScroll(self, start, direction, data):
          if (start < 0) or (start > 15):
             return
          if (start + len(data) > 16):
             return
          for x in range(start, start+len(data)):
              for y in range(7):
                  if direction:
                     self.TileMap[y*16+x] = self.TileMap[(y+1)*16+x]
                  else:
                     self.TileMap[(7-y)*16+x] = self.TileMap[(6-y)*16+x]
              if direction:
                 self.TileMap[112+x] = data[x-start]
              else:
                 self.TileMap[x] = data[x-start]
          self.Display.SetWriteWindow(0, 7, start*8, (start+len(data))*8-1)
          for y in range(8):
              for x in range(start, start+len(data)):
                  i = self.TileMap[y*16+x]
                  self.Display.SendData(self.Tiles[i*8:i*8+8])
                  
