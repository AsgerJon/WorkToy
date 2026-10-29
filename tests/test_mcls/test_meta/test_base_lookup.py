"""
TestBaseLookup pins that the metaclass machinery reads what a base class
holds with 'type.__getattribute__', so a base whose metaclass answers
every name in '__getattr__' cannot answer for it: the '__skip_hash__' flag
the class hash reads, and the '__namespace__' that 'getMROSpace' collects.
Both used to be read with 'getattr', so such a base dropped out of the
hash of its subclasses and contributed a namespace it never had.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from types import SimpleNamespace
from typing import TYPE_CHECKING

from worktoy.mcls import BaseMeta, BaseObject

from .. import MCLSTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Answering(type):
  """Answering answers every name its classes lack with a stand-in
  holding a compiled namespace of its own."""

  def __getattr__(cls, name: str) -> Any:
    return SimpleNamespace(__compiled_space__={'trolled': True})


class Mixin(metaclass=Answering):
  """Mixin is a plain base whose metaclass answers every name."""


class Both(BaseMeta, Answering):
  """Both combines 'BaseMeta' with the metaclass of 'Mixin'."""


class Foo(Mixin, BaseObject, metaclass=Both):
  """Foo subclasses the plain base and 'BaseObject'."""


class TestBaseLookup(MCLSTest):
  """
  TestBaseLookup provides tests for a base whose metaclass answers every
  name.
  """

  def test_hash_keeps_base(self) -> None:
    """The base stays in the class hash: its metaclass cannot claim
    '__skip_hash__' for it."""
    expected = hash(('Foo', 'Mixin', 'BaseObject', 'Both'))
    self.assertEqual(hash(Foo), expected)

  def test_mro_space_skips_base(self) -> None:
    """The base contributes no namespace: its metaclass cannot claim
    '__namespace__' for it."""
    mroSpace = Foo.__namespace__.getMROSpace()
    self.assertNotIn('trolled', mroSpace)
    self.assertIn('__init__', mroSpace)
