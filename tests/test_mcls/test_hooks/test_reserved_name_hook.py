"""
TestReservedNameHook tests the 'ReservedNameHook' from the
'worktoy.mcls.hooks' module.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.waitaminute.meta import ReservedName
from .. import MCLSTest
from worktoy.mcls import AbstractMetaclass
from worktoy.mcls.space_hooks import ReservedNames

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias

  Bases: TypeAlias = tuple[type, ...]


class TestReservedNameHook(MCLSTest):
  """
  TestReservedNameHook tests the 'ReservedNameHook' from the
  'worktoy.mcls.hooks' module.
  """

  def test_repeated_reserved_name(self) -> None:
    """
    The names listed as reserved names are expected to be set at most
    once. Thus, an exception should be expected only upon repeated
    assignments to the same reserved name.
    """

    susModule = """I'm the module, trust me bro!"""
    with self.assertRaises(ReservedName) as context:
      class SusModule(metaclass=AbstractMetaclass):
        """A class to test reserved names."""
        __module__ = susModule
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.resName, '__module__')

  def test_str_repr_reserved_names(self) -> None:
    """
    Test the string representation of the ReservedNames descriptor.
    """

    class Foo:
      names = ReservedNames()

    foo = Foo()
    self.assertIsInstance(foo.names, tuple)
    for name in foo.names:
      self.assertIsInstance(name, str)
    self.assertIsInstance(Foo.names, ReservedNames)
