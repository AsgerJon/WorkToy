"""
TestDispatcher provides tests for the 'TypeSignature' class from the
'worktoy.dispatch' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import TypeSignature, Dispatcher
from worktoy.utilities import stringList, textFmt
from worktoy.waitaminute.dispatch import HashMismatch, CastMismatch
from . import DispatcherTest


def funcIntInt(x: int, y: int) -> int:
  return x + y


def funcInt(x: int) -> int:
  return x


def funcStr(x: str) -> str:
  return x


class TestDispatcher(DispatcherTest):
  """
  TestDispatcher provides tests for the 'TypeSignature' class from the
  'worktoy.dispatch' package.
  """

  def setUp(self, ) -> None:
    self.sigFunc = {
        TypeSignature(int, int): funcIntInt,
        TypeSignature(int)     : funcInt,
        TypeSignature(str)     : funcStr,
    }
    self.sigIntInt = TypeSignature(int, int)
    self.sigInt = TypeSignature(int)
    self.sigStr = TypeSignature(str)

  def test_dict_keys_in(self) -> None:
    """Tests that 'sigFunc' contains the expected keys."""
    self.assertIn(self.sigIntInt, self.sigFunc)
    self.assertIn(self.sigInt, self.sigFunc)
    self.assertIn(self.sigStr, self.sigFunc)

  def test_dict_getitem(self) -> None:
    """Tests that 'sigFunc' returns the expected functions."""
    self.assertIs(self.sigFunc[self.sigIntInt], funcIntInt)
    self.assertIs(self.sigFunc[self.sigInt], funcInt)
    self.assertIs(self.sigFunc[self.sigStr], funcStr)

  def test_from_args(self, ) -> None:
    """Tests that 'TypeSignature.from_args' returns the expected function."""
    fromIntInt = TypeSignature.fromArgs(69, 420)
    fromInt = TypeSignature.fromArgs(1337)
    fromStr = TypeSignature.fromArgs('lol')
    self.assertEqual(fromIntInt, self.sigIntInt)
    self.assertEqual(fromInt, self.sigInt)
    self.assertEqual(fromStr, self.sigStr)

  def test_good_fast(self, ) -> None:
    """Test that TypeSignature instances correctly identifies arguments of
    correct types"""
    expected = 69, 420
    actual = self.sigIntInt.fast(69, 420)
    self.assertEqual(actual, expected)

    expected = 1337,
    actual = self.sigInt.fast(1337)
    self.assertEqual(actual, expected)

    expected = 'lol',
    actual = self.sigStr.fast('lol')
    self.assertEqual(actual, expected)

  def test_bad_fast(self, ) -> None:
    """Test that TypeSignature instances correctly raises exceptions for
    arguments of incorrect types"""
    #  Bad types
    with self.assertRaises(HashMismatch) as context:
      self.sigIntInt.fast(69, '420')
    e = context.exception
    self.assertIs(e.sig, self.sigIntInt)
    self.assertEqual(e.args, (69, '420'))
    self.assertEqual(str(e), repr(e))
    #  Too many arguments
    with self.assertRaises(HashMismatch) as context:
      self.sigIntInt.fast(69, 420, 1337)
    e = context.exception
    self.assertIs(e.sig, self.sigIntInt)
    self.assertEqual(e.args, (69, 420, 1337))
    self.assertEqual(str(e), repr(e))
    #  Too few arguments
    with self.assertRaises(HashMismatch) as context:
      self.sigIntInt.fast()
    e = context.exception
    self.assertIs(e.sig, self.sigIntInt)
    self.assertFalse(e.args)
    self.assertEqual(str(e), repr(e))

  def test_good_cast(self, ) -> None:
    """Test that TypeSignature instances correctly casts arguments of
    castable types"""
    #  Exactly correct types
    expected = 69, 420
    actual = self.sigIntInt.cast(69, 420)
    self.assertEqual(actual, expected)
    #  Castable types
    args = '69', '420'
    expected = 69, 420
    actual = self.sigIntInt.cast(*args)
    self.assertEqual(actual, expected)
    #  Castable types with different types
    args = 69.0, 420.0
    expected = 69, 420
    actual = self.sigIntInt.cast(*args)
    self.assertEqual(actual, expected)
    #  Mixed types
    args = 69.0, '420'
    expected = 69, 420
    actual = self.sigIntInt.cast(*args)
    self.assertEqual(actual, expected)

  def test_bad_cast(self, ) -> None:
    """Test that TypeSignature instances correctly raises exceptions for
    arguments of uncastable types"""
    #  Too few arguments
    with self.assertRaises(CastMismatch) as context:
      self.sigIntInt.cast(69.0)
    e = context.exception
    self.assertIs(e.sig, self.sigIntInt)
    self.assertEqual(e.args, (69.0,))
    #  Too many arguments
    with self.assertRaises(CastMismatch) as context:
      self.sigIntInt.cast(69.0, 420.0, 1337.0)
    e = context.exception
    self.assertIs(e.sig, self.sigIntInt)
    #  Uncastable values
    with self.assertRaises(CastMismatch) as context:
      self.sigInt.cast('sixty-nine')
    e = context.exception
    self.assertIs(e.sig, self.sigInt)
    self.assertEqual(e.args, ('sixty-nine',))
    #  Uncastable target (str)
    with self.assertRaises(CastMismatch) as context:
      self.sigStr.cast(69)
    e = context.exception
    self.assertIs(e.sig, self.sigStr)
    self.assertEqual(e.args, (69,))

  def test_coverage_gymnastics(self) -> None:
    self.assertEqual(len(self.sigIntInt), 2)
    self.assertEqual(len(self.sigInt), 1)
    self.assertEqual(len(self.sigStr), 1)

    self.assertEqual(69 + 420, self.sigFunc[self.sigIntInt](69, 420))
    self.assertEqual(1337, self.sigFunc[self.sigInt](1337))
    self.assertEqual('lol', self.sigFunc[self.sigStr]('lol'))

    for item in self.sigIntInt:
      self.assertIs(item, int)

    for item in self.sigInt:
      self.assertIs(item, int)

    for item in self.sigStr:
      self.assertIs(item, str)

    self.assertFalse(self.sigIntInt == 'breh')
    self.assertFalse(self.sigInt == 'breh')
    self.assertFalse(self.sigStr == 'breh')

    longSig = TypeSignature.fromArgs(*stringList("""
    Never, gonna, give, you, up
    """))

    self.assertFalse(self.sigIntInt == 'breh')
    self.assertFalse(self.sigInt == 'breh')
    self.assertFalse(self.sigStr == 'breh')

    self.assertFalse(self.sigIntInt == longSig)
    self.assertFalse(self.sigInt == longSig)
    self.assertFalse(self.sigStr == longSig)

    sigFloatFloat = TypeSignature(float, float)
    sigFloat = TypeSignature(float)

    self.assertFalse(self.sigIntInt == sigFloatFloat)
    self.assertFalse(self.sigInt == sigFloat)
    self.assertFalse(self.sigStr == sigFloat)

    self.assertIn(float, sigFloat)
    self.assertIn(float, sigFloatFloat)
    self.assertNotIn(int, sigFloat)
    self.assertNotIn(int, sigFloatFloat)

    self.assertGreater(len(str(sigFloatFloat)), len(str(sigFloat)))
    self.assertGreater(len(repr(sigFloatFloat)), len(repr(sigFloat)))

  def test_mro_len(self) -> None:
    """Test that the MRO length of TypeSignature is 1."""
    testTypes = (int, float, str, bool, tuple, list, dict, set, frozenset,)
    for type_ in testTypes:
      print("""Testing MRO length for type: %s""" % type_)
      try:
        sig = TypeSignature(type_)
        n = sig.mroLen()
      except Exception as exception:
        infoSpec = """Caught %s: %s"""
        excType = type(exception).__name__
        excStr = str(exception)
        info = infoSpec % (excType, excStr)
        print(textFmt(info))
      else:
        print("""MRO length for type %s: %d""" % (type_, n))
      finally:
        print('-' * 40)
