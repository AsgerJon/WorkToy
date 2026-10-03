"""
TestOverloadOwnerRefused subclasses 'OverloadTest' and pins that a
declared signature refuses 'OWNER', which plays no role in overload
signatures, with 'TypeError' at the declaration. 'OWNER' passes the
test of being a class, so it used to build the class, and every call
then failed hashing the signature it was left in.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, OWNER, THIS
from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import BaseObject

from . import OverloadTest


class TestOverloadOwnerRefused(OverloadTest):
  """
  TestOverloadOwnerRefused provides tests for 'OWNER' in a declared
  signature.
  """

  def test_owner_refused(self) -> None:
    """'OWNER', alone or after another entry, raises 'TypeError' that
    names 'THIS' as the sentinel for the class itself."""
    for types in ((OWNER,), (int, OWNER)):
      with self.subTest(types=types):
        with self.assertRaises(TypeError) as context:
          overload(*types)
        self.assertIn('OWNER', str(context.exception))
        self.assertIn('THIS', str(context.exception))

  def test_args_of_owner_refused(self) -> None:
    """An 'ARGS' of 'OWNER' raises 'TypeError'."""
    with self.assertRaises(TypeError):
      overload(ARGS[OWNER])

  def test_dispatcher_refuses_owner(self) -> None:
    """'Dispatcher.overload' refuses 'OWNER' as well."""
    with self.assertRaises(TypeError):
      Dispatcher().overload(OWNER)

  def test_this_accepted(self) -> None:
    """'THIS' is still accepted."""

    class Foo(BaseObject):
      @overload(THIS)
      def bar(self, other: Foo) -> str:
        return 'this'

    self.assertEqual(Foo().bar(Foo()), 'this')
