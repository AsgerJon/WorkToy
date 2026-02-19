"""
TestAttributeErrorFactory is a factory for creating AttributeError instances.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import WaitAMinuteTest
from worktoy.waitaminute import attributeErrorFactory

if TYPE_CHECKING:  # pragma: no cover
  pass


class Foo:
  pass


class TestAttributeErrorFactory(WaitAMinuteTest):
  """
  TestAttributeErrorFactory is a factory for creating AttributeError
  instances.
  """

  def test_create(self) -> None:
    """
    Test the creation of an AttributeError instance.
    """
    with self.assertRaises(AttributeError):
      raise attributeErrorFactory(Foo(), 'breh')
    with self.assertRaises(AttributeError):
      raise attributeErrorFactory('coverage', 'is fun')
