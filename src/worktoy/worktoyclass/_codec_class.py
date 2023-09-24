"""WorkToy - WorkToyClass - CodecClass
Enhances the WorkToyClass with codecs. """
#  MIT Licence
#  Copyright (c) 2023 Asger Jon Vistisen
from __future__ import annotations

from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from worktoy.worktoyclass import StringTools

AlignFlag = Qt.AlignmentFlag


class CodecClass(StringTools):
  """WorkToy - WorkToyClass - Codec
  Enhances the WorkToyClass with codecs. """

  def __init__(self, *args, **kwargs) -> None:
    StringTools.__init__(self, *args, **kwargs)

  def hexify(self, value: int) -> str:
    """Returns a string representation of the value given in HEX code."""
    if not value:
      return '00'
    H = self.stringList('0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F')
    hexMap = {i: h for (i, h) in enumerate(H)}
    NEX = []
    while value > 0:
      NEX.append(value % 16)
      value -= NEX[-1]
      value = int(value / 16)
    hexCode = ''
    NEX.reverse()
    for h in NEX:
      hexCode += hexMap[h]
    return hexCode

  def unHexify(self, hexValue: str) -> int:
    """Converts the hexValue to int. """
    hexValue = hexValue.upper()
    H = self.stringList('0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F')
    hexMap = {h: i for (i, h) in enumerate(H)}
    hexDigs = reversed([char for char in hexValue])
    out = 0
    c = 0
    for char in hexDigs:
      out += (hexMap[char] * 16 ** c)
      c += 1
    return out

  def encodeQColor(self, color: QColor) -> str:
    """QColor encoder"""
    r, g, b, a = color.red(), color.green(), color.blue(), color.alpha()
    R, G, B, A = [self.hexify(i) for i in [r, g, b, a]]
    return '#%s%s%s%s' % (R, G, B, A)

  def decodeQColor(self, color: str) -> QColor:
    """Color specified"""
    if len(color) == 7:
      color += 'FF'
    R, G, B, A = color[1:3], color[3:5], color[5:7], color[7:]
    r = self.unHexify(R)
    g = self.unHexify(G)
    b = self.unHexify(B)
    a = self.unHexify(A)
    return QColor(r, g, b, a)

  def encodeInt(self, intValue: int) -> str:
    """Encodes integer"""
    return '%d' % intValue

  def decodeInt(self, data: str) -> int:
    """Decodes to integer"""
    if data is None:
      return 0
    digs = {str(i): i for i in range(10)}
    data = [c for c in reversed(data) if digs.get(c, None) is not None]
    out = 0
    for i, char in enumerate(data):
      num = digs.get(char, None)
      if num is not None:
        out += (num * 10 ** i)
    return out

  def decodeFloat(self, data: str) -> float:
    """Decodes to float"""
    if '.' not in data:
      if ',' not in data:
        if ';' not in data:
          if '|' not in data:
            data = '%s.0' % data
          else:
            data = data.replace('|', '.')
        else:
          data = data.replace(';', '.')
      else:
        data = data.replace(',', '.')
    digs = ['%d' % i for i in range(10)] + ['.', ]
    data = [char for char in data if char in digs]
    data = ''.join(data)
    left, right = data.split('.')[:2]
    n = len(right)
    intVal = self.decodeInt(data)
    return intVal * 10 ** (-n)

  def encodeBool(self, data: bool) -> str:
    """Encodes boolean values"""
    return 'true' if data else 'false'

  def decodeBool(self, booleanString: str) -> bool:
    """Encodes string to boolean value"""
    if booleanString == 'true':
      return True
    if booleanString == 'false':
      return False
    raise ValueError

  def isLog2(self, val: int) -> bool:
    """determines if val is a log2"""
    if val < 1:
      return False
    if val == 1:
      return True
    if val % 2:
      return False
    return self.isLog2(int(val / 2))

  def log2ceil(self, intVal: int) -> int:
    """Log"""
    if not intVal:
      raise ZeroDivisionError
    if intVal < 0:
      raise ValueError
    if intVal == 1:
      return 1
    out = 2
    c = 0
    while out * 2 ** c < intVal:
      c += 1
    return c

  def toBinary(self, intVal: int) -> Any:
    """Converts the value to the binary"""
    out = []
    while intVal:
      out.append(int(intVal % 2))
      intVal -= out[-1]
      intVal /= 2
    return [i for i in reversed(out)]
