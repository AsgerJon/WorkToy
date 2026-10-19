"""
TestArgsRegistered subclasses 'CoreTest' and pins that the 'ARGS'
sentinel is registered with 'SentinelMeta' like every other sentinel, so
a second class statement at its name is refused with 'DuplicateSentinel'.
Its metaclass used to build the class with 'type.__new__' directly, which
skipped the registry, so 'ARGS' alone could be declared twice.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, SentinelMeta
from worktoy.core.sentinels._args import _MetaARGS
from worktoy.waitaminute.meta import DuplicateSentinel

from . import CoreTest


class TestArgsRegistered(CoreTest):
  """
  TestArgsRegistered provides tests for the registration of 'ARGS'.
  """

  def test_registered_by_name(self) -> None:
    """The registry holds 'ARGS' under its name."""
    self.assertIs(SentinelMeta._getNamedSentinel('ARGS'), ARGS)
    registered = SentinelMeta._getRegisteredSentinels()
    self.assertTrue(any(sentinel is ARGS for sentinel in registered))

  def test_second_args_refused(self) -> None:
    """A second class statement at the name 'ARGS' is refused, naming
    the existing sentinel."""
    with self.assertRaises(DuplicateSentinel) as context:
      _MetaARGS('ARGS', (), {'__module__': __name__})
    self.assertIs(context.exception.existing, ARGS)

  def test_still_instantiable(self) -> None:
    """Registration leaves the subscript, and so instantiation, as it
    was."""
    self.assertIs(ARGS[int].__inner_type__, int)
    self.assertEqual(ARGS[int], ARGS[int])
