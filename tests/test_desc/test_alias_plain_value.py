"""
TestAliasPlainValue subclasses 'DescTest' and pins what an 'Alias' does
when the name it stands for resolves only after the class exists and
holds a plain value rather than a descriptor: a read returns the value, a
write raises 'ReadOnlyError' and a deletion 'ProtectedError'. The alias
used to call '__get__' on the value, which an 'int' does not have, so
the read failed with a bare 'AttributeError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Alias
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import ProtectedError, ReadOnlyError

from . import DescTest


class TestAliasPlainValue(DescTest):
  """
  TestAliasPlainValue provides tests for an alias of a plain value
  supplied after class creation.
  """

  def test_read_returns_value(self) -> None:
    """The alias stays in place and a read gives the value, on the
    instance and on the class."""

    class Owner(BaseObject):
      v = Alias('later')

    self.assertIsInstance(Owner.__dict__['v'], Alias)
    Owner.later = 5
    self.assertEqual(Owner().v, 5)
    self.assertEqual(Owner.v, 5)

  def test_write_and_delete_refused(self) -> None:
    """A plain value cannot be written or deleted through the alias."""

    class Owner(BaseObject):
      v = Alias('later')

    Owner.later = 5
    owner = Owner()
    with self.assertRaises(ReadOnlyError):
      owner.v = 6
    with self.assertRaises(ProtectedError):
      del owner.v
    self.assertEqual(owner.v, 5)

  def test_function_binds(self) -> None:
    """A function supplied later binds as a method, as before."""

    class Owner(BaseObject):
      v = Alias('later')

    Owner.later = lambda self: 'bound'
    self.assertEqual(Owner().v(), 'bound')
