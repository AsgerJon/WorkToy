"""
TestThisSignature subclasses 'OverloadTest' and pins that a signature
naming 'THIS', whether as an entry or as the inner type of a trailing
'ARGS', matches instances of the class and nothing else. The cast passes
used to call the class on the argument, and 'Object.__init__' accepts
anything, so '@overload(THIS)' on a class without a constructor of its
own took every argument there is, as a freshly built instance; 'typeCast'
now calls no constructor, and a class that wants to be cast to declares
'__cast_as__'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, THIS
from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import OverloadTest


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


class TestThisSignature(OverloadTest):
  """
  TestThisSignature provides tests for 'THIS' signatures.
  """

  def test_instance_matches(self) -> None:
    """An instance of the class matches every form."""
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
