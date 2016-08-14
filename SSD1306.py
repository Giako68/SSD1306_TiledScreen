#
# Simple SSD1306 driver for ESP8266 & MicroPython
#
# Startup Sequence:
# 0x8D,0x14: Enable Charge Pump.
# 0x81,0xCF: Set Contrast Control.
# 0xD9,0xF1: Set Pre-charge Period.
# 0xDB,0x40: Set VCOMH Deselect Level
# 0x2E:      Deactivate scroll.
# 0xAF:      Set Display ON.
#

from machine import Pin, I2C
from ustruct import pack

class SSD1306(object):
      def __init__(self, scl, sda, addr):
          self.Bus = I2C(scl=Pin(scl), sda=Pin(sda), freq=400000)
          self.Addr = addr
          self.SendCommand(pack("10B",  0x8D,0x14,0x81,0xCF,0xD9,0xF1,0xDB,0x40,0x2E,0xAF))
          
      def SendCommand(self, Cmd):
          Msg = pack("BB", self.Addr<<1, 0x00) + Cmd
          self.Bus.start()
          self.Bus.write(Msg)
          self.Bus.stop()

      def SendData(self, Data):
          Msg = pack("BB", self.Addr<<1, 0x40) + Data
          self.Bus.start()
          self.Bus.write(Msg)
          self.Bus.stop()

      def SetHorizontalAddressingMode(self):
          self.SendCommand(pack("BB", 0x20, 0x00))

      def SetVerticalAddressingMode(self):
          self.SendCommand(pack("BB", 0x20, 0x01))

      def SetPageAddressingMode(self):
          self.SendCommand(pack("BB", 0x20, 0x02))
          
      def SetSegmentRemap(self, Flag):
          if (Flag):
             self.SendCommand(pack("B", 0xA1))
          else:
             self.SendCommand(pack("B", 0xA0))

      def SetScanDirection(self, Flag):
          if (Flag):
             self.SendCommand(pack("B", 0xC8))
          else:
             self.SendCommand(pack("B", 0xC0))

      def SetWriteWindow(self, PageStart, PageStop, ColStart, ColStop):
          if (PageStart < 0) or (PageStop > 7) or (PageStart > PageStop):
             return(-1)
          if (ColStart < 0) or (ColStop > 127) or (ColStart > ColStop):
             return(-1)
          self.SendCommand(pack("6B", 0x21, ColStart, ColStop, 0x22, PageStart, PageStop))
          return(0)
