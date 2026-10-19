"""
TestThisStrictDefault subclasses 'OverloadTest' and pins that a signature
naming 'THIS', whether as an entry or as the inner type of a trailing
'ARGS', refuses casts unless declared with 'strict=False'. The cast
passes used to call the class on the argument, and 'Object.__init__'
accepts anything, so '@overload(THIS)' on a class without a constructor
of its own took every argument there is, as a freshly built instance.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, THIS
from worktoy.dispatch import Dispatcher, overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import OverloadTest


def _one(self, other) -> str:
  return type(other).__name__


class Plain(BaseObject):
  """A class without a constructor of its own, so 'Plain(x)' accepts any
  'x'."""

  @overload(THIS)
  def same(self, other: Plain) -> str:
    return 'same'

  @overload(THIS, int)
  def pair(self, other: Plain, n: int) -> str:
    return 'pair'

  @overload(ARGS[THIS])
  def many(self, *others: Plain) -> int:
    return len(others)

  @overload(THIS, strict=False)
  def loose(self, other: Plain) -> str:
    return 'loose'


class TestThisStrictDefault(OverloadTest):
  """
  TestThisStrictDefault provides tests for the strictness of 'THIS'
  signatures.
  """

  def test_instance_matches(self) -> None:
    """An instance of the class still matches every form."""
    plain = Plain()
    self.assertEqual(plain.same(Plain()), 'same')
    self.assertEqual(plain.pair(Plain(), 1), 'pair')
    self.assertEqual(plain.many(Plain(), Plain()), 2)

  def test_other_argument_refused(self) -> None:
    """Anything but an instance is refused instead of being built."""
    plain = Plain()
    for arg in (42, 'x', None, object()):
      with self.subTest(arg=arg):
        with self.assertRaises(DispatchException):
          plain.same(arg)
        with self.assertRaises(DispatchException):
          plain.pair(arg, 1)
        with self.assertRaises(DispatchException):
          plain.many(arg)

  def test_strict_false_casts(self) -> None:
    """'strict=False' asks for the cast, which builds the instance."""
    self.assertEqual(Plain().loose(42), 'loose')

  def test_flags(self) -> None:
    """The signatures carry the flag the dispatcher reads."""
    sigs = {
      name: Plain.__dict__[name]._getDeclaredSigs()[0]
      for name in ('same', 'pair', 'many', 'loose')
    }
    self.assertFalse(sigs['same'].__allow_flex__)
    self.assertFalse(sigs['pair'].__allow_flex__)
    self.assertFalse(sigs['many'].__allow_flex__)
    self.assertTrue(sigs['loose'].__allow_flex__)

  def test_other_signatures_unchanged(self) -> None:
    """A signature without 'THIS' still allows casts by default."""
    (sig, _), = [*overload(int)(_one)]
    self.assertTrue(sig.__allow_flex__)

  def test_dispatcher_method(self) -> None:
    """'Dispatcher.overload' applies the same default and keyword."""
    dispatcher = Dispatcher()
    dispatcher.overload(THIS)(_one)
    dispatcher.overload(int, THIS, strict=False)(_one)
    strictSig, looseSig = dispatcher._getDeclaredSigs()
    self.assertFalse(strictSig.__allow_flex__)
    self.assertTrue(looseSig.__allow_flex__)
