"""
TestDispatcher provides tests for the 'TypeSig' class from the
'worktoy.dispatch' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import TypeSig, Dispatcher, overload
from worktoy.utilities import stringList, textFmt
from . import DispatcherTest


def funcIntInt(x: int, y: int) -> int:
  return x + y


def funcInt(x: int) -> int:
  return x


def funcStr(x: str) -> str:
  return x


class TestDispatcher(DispatcherTest):
  """
  TestDispatcher provides tests for the 'TypeSig' class from the
  'worktoy.dispatch' package.
  """

  def setUp(self, ) -> None:
    self.sigFunc = {
      TypeSig(int, int): funcIntInt,
      TypeSig(int): funcInt,
      TypeSig(str): funcStr,
      }
    self.sigIntInt = TypeSig(int, int)
    self.sigInt = TypeSig(int)
    self.sigStr = TypeSig(str)

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
    """Tests that 'TypeSig.from_args' returns the expected function."""
    fromIntInt = TypeSig.fromArgs(69, 420)
    fromInt = TypeSig.fromArgs(1337)
    fromStr = TypeSig.fromArgs('lol')
    self.assertEqual(fromIntInt, self.sigIntInt)
    self.assertEqual(fromInt, self.sigInt)
    self.assertEqual(fromStr, self.sigStr)

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

    longSig = TypeSig.fromArgs(
      *stringList(
        """
            Never, gonna, give, you, up
            """,
        ),
      )

    self.assertFalse(self.sigIntInt == 'breh')
    self.assertFalse(self.sigInt == 'breh')
    self.assertFalse(self.sigStr == 'breh')

    self.assertFalse(self.sigIntInt == longSig)
    self.assertFalse(self.sigInt == longSig)
    self.assertFalse(self.sigStr == longSig)

    sigFloatFloat = TypeSig(float, float)
    sigFloat = TypeSig(float)

    self.assertFalse(self.sigIntInt == sigFloatFloat)
    self.assertFalse(self.sigInt == sigFloat)
    self.assertFalse(self.sigStr == sigFloat)

    self.assertIn(float, sigFloat)
    self.assertIn(float, sigFloatFloat)
    self.assertNotIn(int, sigFloat)
    self.assertNotIn(int, sigFloatFloat)

    self.assertGreater(len(str(sigFloatFloat)), len(str(sigFloat)))
    self.assertGreater(len(repr(sigFloatFloat)), len(repr(sigFloat)))

  def test_clone_fallback(self) -> None:
    """Tests that 'TypeSig.clone' returns a new instance."""

    class Parent:
      foo = Dispatcher()

      @foo.fallback
      def foo(self, *args, **kwargs):
        return 'fallback'

    class Child(Parent):
      foo = Parent.foo.clone()

      @foo.overload(int, int, int)
      def foo(self, x: int, y: int, z: int) -> str:
        infoSpec = """%s(%d, %d, %d)"""
        info = infoSpec % (type(self).__name__, x, y, z)
        return textFmt(info)

    self.assertEqual(Parent().foo('breh'), 'fallback')
    self.assertEqual(Child().foo(69, 420, 1337), 'Child(69, 420, 1337)')

  def test_overload_call(self, ) -> None:
    """Tests that 'overload' created intermediate objects correctly raises
    TypeError when called."""

    def func() -> None:
      """Placeholder function."""

    sig = TypeSig(int, int)
    load = overload(sig, func)

    with self.assertRaises(TypeError):
      _ = load(69, 420)  # NOQA, it's okay pycharm, 'unreachable' i kno.
