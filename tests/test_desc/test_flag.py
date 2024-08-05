"""TestFlag tests the use of Flag as a replacement for 'bool'."""
#  AGPL-3.0 license
#  Copyright (c) 2024 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.parse import maybe


class Byte:
  """Using 8 Flag, I mean bool"""

  x0 = AttriBox[bool](False)
  x1 = AttriBox[bool](False)
  x2 = AttriBox[bool](False)
  x3 = AttriBox[bool](False)
  x4 = AttriBox[bool](False)
  x5 = AttriBox[bool](False)
  x6 = AttriBox[bool](False)
  x7 = AttriBox[bool](False)

  def __init__(self, value: int = None) -> None:
    value = maybe(value, 0)
    self.x0 = bool(value & 1)
    self.x1 = bool(value & 2)
    self.x2 = bool(value & 4)
    self.x3 = bool(value & 8)
    self.x4 = bool(value & 16)
    self.x5 = bool(value & 32)
    self.x6 = bool(value & 64)
    self.x7 = bool(value & 128)

  def __str__(self) -> str:
    """Hex representation"""
    return '0x%02x' % self.__int__()

  def _getXs(self) -> list[bool]:
    """Get the values of the flags"""
    return [
        self.x0,
        self.x1,
        self.x2,
        self.x3,
        self.x4,
        self.x5,
        self.x6,
        self.x7
    ]

  def __int__(self) -> int:
    """Int representation"""
    out = 0
    for (i, x) in enumerate(self._getXs()):
      out += (2 ** i if x else 0)
    return out

  def __bool__(self) -> bool:
    """Bool representation"""
    return True if int(self) else False


class TestFlag(TestCase):
  """TestFlag tests the use of Flag as a replacement for 'bool'."""

  def setUp(self) -> None:
    self.lolByte = Byte(69)
    self.lmaoByte = Byte()

  def testVal(self) -> None:
    """Test the value of the Byte"""
    self.assertEqual(int(self.lolByte), 69)
    self.assertEqual(int(self.lmaoByte), 0)

  def testSet(self) -> None:
    """Tests if the setter applies correctly"""
    self.assertEqual(int(self.lmaoByte), 0)
    self.lmaoByte.x0 = True
    self.assertEqual(int(self.lmaoByte), 1)
