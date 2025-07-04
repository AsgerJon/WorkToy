"""
TestMetaUmbrella covers obscure edge cases and esoteric fallbacks of the
AbstractMetaclass from the worktoy.mcls module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.mcls import AbstractMetaclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Self


class Foo(metaclass=AbstractMetaclass):
  """Foo implements neither __class_eq__ nor __class_ne__."""
  pass


class Bar(Foo):
  """Bar does implement __class_ne__, but not __class_eq__."""

  @classmethod
  def __class_ne__(cls, other: Any) -> bool:
    if other is Foo:
      return True
    return NotImplemented


class TestMetaUmbrella(TestCase):
  """
  TestMetaUmbrella covers obscure edge cases and esoteric fallbacks of the
  AbstractMetaclass from the worktoy.mcls module.
  """

  @classmethod
  def tearDownClass(cls) -> None:
    import sys
    import gc
    sys.modules.pop(__name__, None)
    gc.collect()

  def testClassEquality(self) -> None:
    """
    Test that classes without __class_eq__ or __class_ne__ fall back to
    default equality checks.
    """
    self.assertTrue(Foo == Foo)
    self.assertFalse(Foo != Foo)
    self.assertFalse(Foo == 69, 420)
    self.assertTrue(Bar != Foo)
    self.assertFalse(Bar != Bar)
