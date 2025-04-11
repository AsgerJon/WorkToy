"""TestTypeSig tests that TypeSig casts correctly. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import TypeSig
from worktoy.waitaminute import SigMismatch


class Breh:
  """LMAO"""

  def __getitem__(self, *args, **kwargs) -> None:
    """LMAO"""
    if not kwargs.get('_root', False):
      if isinstance(args[0], tuple) and len(args) == 1:
        return self.__getitem__(*args[0], _root=True)
    print(args)


class TestTypeSig(TestCase):
  """TestTypeSig tests that TypeSig casts correctly. """

  def test_init(self, ) -> None:
    """Tests that the TypeSig class is initialized correctly."""

    point3DInt = TypeSig(int, int, int)
    point3DFloat = TypeSig(float, float, float)
    point3DStr = TypeSig(str, str, str)

    intStr = '%s' % (point3DInt,)
    floatStr = '%s' % (point3DFloat,)
    strStr = '%s' % (point3DStr,)

    intExpectStr = 'TypeSig object: [int, int, int]'
    floatExpectStr = 'TypeSig object: [float, float, float]'
    strExpectStr = 'TypeSig object: [str, str, str]'

    intExpectRepr = 'TypeSig(int, int, int)'
    floatExpectRepr = 'TypeSig(float, float, float)'
    strExpectRepr = 'TypeSig(str, str, str)'

    self.assertEqual(intStr, intExpectStr)
    self.assertEqual(floatStr, floatExpectStr)
    self.assertEqual(strStr, strExpectStr)
    self.assertEqual(repr(point3DInt), intExpectRepr)
    self.assertEqual(repr(point3DFloat), floatExpectRepr)
    self.assertEqual(repr(point3DStr), strExpectRepr)

  def test_fast_cast(self) -> None:
    """Tests that the TypeSig class casts correctly."""

    point3DInt = TypeSig(int, int, int)
    point3DFloat = TypeSig(float, float, float)
    point3DStr = TypeSig(str, str, str)

    self.assertEqual(point3DInt.fast(1, 2, 3), (1, 2, 3))
    self.assertEqual(point3DFloat.fast(1.0, 2.0, 3.0), (1.0, 2.0, 3.0))
    self.assertEqual(point3DStr.fast('a', 'b', 'c'), ('a', 'b', 'c'))

  def test_normal_cast(self, ) -> None:
    """Tests that the TypeSig class casts correctly."""

    point3DInt = TypeSig(int, int, int)
    point3DFloat = TypeSig(float, float, float)
    point3DStr = TypeSig(str, str, str)

    intArgs = (69, 420, 1337)
    floatArgs = (69.0, 420.0, 1337.0)
    strArgs = ('69', '420', '1337')
    mixArgs = (69, 420.0, '1337')

    intExpect = (69, 420, 1337)
    floatExpect = (69.0, 420.0, 1337.0)
    strExpect = ('69', '420', '1337')

    self.assertEqual(point3DInt.cast(*intArgs), intExpect)
    self.assertEqual(point3DInt.cast(*floatArgs), intExpect)
    self.assertEqual(point3DInt.cast(*strArgs), intExpect)
    self.assertEqual(point3DInt.cast(*mixArgs), intExpect)

    self.assertEqual(point3DFloat.cast(*intArgs), floatExpect)
    self.assertEqual(point3DFloat.cast(*floatArgs), floatExpect)
    self.assertEqual(point3DFloat.cast(*strArgs), floatExpect)
    self.assertEqual(point3DFloat.cast(*mixArgs), floatExpect)

    self.assertEqual(point3DStr.cast(*intArgs), strExpect)
    self.assertEqual(point3DStr.cast(*strArgs), strExpect)

  def test_flex(self, ) -> None:
    """Tests that the TypeSig class casts correctly."""

    mixSig = TypeSig(int, float, str)

    intArgs = (69, 420, 1337)
    floatArgs = (69.0, 420.0, 1337.0)
    strArgs = ('69', '420', '1337')
    mixArgs = [intArgs, floatArgs, strArgs, ]

    mixExpect = (69, 420.0, '1337')

    for i in range(3):
      for j in range(3):
        for k in range(3):
          testArgs = (mixArgs[i][0], mixArgs[j][1], mixArgs[k][2])
          resArgs = [*mixSig.flex(*testArgs), ]
          resArgs[2] = resArgs[2].replace('.0', '')

          self.assertEqual((*resArgs,), mixExpect)

  def test_errors(self, ) -> None:
    """Tests that the TypeSig class raises errors correctly."""
    point3DInt = TypeSig(int, int, int)
    point3DFloat = TypeSig(float, float, float)
    point3DStr = TypeSig(str, str, str)

    intArgs = (69, 420, 1337)
    floatArgs = (69.0, 420.0, 1337.0)
    strArgs = ('69', '420', '1337')
    mixArgs = (69, 420.0, '1337')

    intExpect = (69, 420, 1337)
    floatExpect = (69.0, 420.0, 1337.0)
    strExpect = ('69', '420', '1337')

    sigs = [point3DInt, point3DFloat, point3DStr]
    args = [intArgs, floatArgs, strArgs]
    expected = [intExpect, floatExpect, strExpect]

    for sig, arg, exp in zip(sigs, args, expected):
      with self.assertRaises(SigMismatch):
        sig.fast(*arg, 'Too many arguments!')
        sig.cast(*arg, 'Too many arguments!')
      with self.assertRaises(SigMismatch):
        sig.fast(*arg[:-1], )  # Too few arguments
        sig.cast(*arg[:-1], )  # Too few arguments
        sig.flex(*arg[:-1], )  # Too few arguments
      with self.assertRaises(SigMismatch):
        sig.fast(mixArgs, )  # Wrong argument type
      castRes = sig.cast(*arg)
      if sig is point3DStr:
        break
      self.assertEqual(castRes, exp)
