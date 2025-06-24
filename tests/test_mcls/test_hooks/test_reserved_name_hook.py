"""
TestReservedNameHook tests the 'ReservedNameHook' from the
'worktoy.mcls.hooks' module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase
from typing import TYPE_CHECKING

from worktoy.mcls import AbstractMetaclass
from worktoy.mcls.hooks import ReservedNames
from worktoy.waitaminute import ReservedName, ReadOnlyError, ProtectedError
from worktoy.waitaminute import _Attribute  # NOQA

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class TestReservedNameHook(TestCase):
  """
  TestReservedNameHook tests the 'ReservedNameHook' from the
  'worktoy.mcls.hooks' module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def test_repeated_reserved_name(self) -> None:
    """
    The names listed as reserved names are expected to be set at most
    once. Thus, an exception should be expected only upon repeated
    assignments to the same reserved name.
    """

    with self.assertRaises(ReservedName) as context:
      class SusModule(metaclass=AbstractMetaclass):
        """A class to test reserved names."""
        __module__ = """I'm the module, trust me bro!"""
    e = context.exception
    self.assertEqual(e.resName, '__module__')

  def test_reserved_name_descriptor_class(self) -> None:
    """
    Testing __set__ and __delete__ methods on the ReservedNames descriptor
    """

    class Foo:
      names = ReservedNames()

    self.assertIs(Foo.names.__field_owner__, Foo)
    self.assertIs(Foo.names.__field_name__, 'names')

    for name in Foo.names:
      self.assertTrue(str.startswith(name, '__'))
      self.assertTrue(str.endswith(name, '__'))
    foo = Foo()
    with self.assertRaises(ReadOnlyError) as context:
      foo.names = 'derp'
    e = context.exception
    self.assertIs(e.owningInstance, foo)
    self.assertIs(e.descriptorObject, Foo.names)
    self.assertEqual(e.existingValue, foo.names)
    self.assertEqual(e.newValue, 'derp')

    with self.assertRaises(ProtectedError) as context:
      del foo.names
    e = context.exception
    self.assertIs(e.owningInstance, foo)
    self.assertIs(e.descriptorObject, Foo.names)
    self.assertIs(e.existingValue, foo.names)

  def test_str_repr_reserved_names(self) -> None:
    """
    Test the string representation of the ReservedNames descriptor.
    """

    class Foo:
      names = ReservedNames()

    foo = Foo()

    strReservedNames = str(foo.names)
    self.assertTrue(strReservedNames.startswith('ReservedNames:'))
    i = 0
    for i, name in enumerate(foo.names):
      self.assertIn(name, strReservedNames)
    self.assertEqual(len(foo.names), i + 1)
