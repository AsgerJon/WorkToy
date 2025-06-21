"""TestZeroton tests the Zeroton metaclass. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static.zeroton import Zeroton, THIS, OWNER, DESC
from worktoy.waitaminute import IllegalInstantiation

try:
  from typing import TYPE_CHECKING
except ImportError:  # pragma: no cover
  try:
    from typing_extensions import TYPE_CHECKING
  except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:
  from typing import Self


class TestZeroton(TestCase):
  """TestZeroton tests the Zeroton metaclass. """

  def test_is_instance(self, ) -> None:
    """Test that the Zeroton metaclass is an instance of itself."""
    self.assertIsInstance(THIS, Zeroton)
    self.assertIsInstance(OWNER, Zeroton)
    self.assertIsInstance(DESC, Zeroton)

  def test_raises(self, ) -> None:
    """Test that the Zeroton metaclass raises the correct exceptions."""
    with self.assertRaises(IllegalInstantiation) as context:
      _ = THIS()
    cls = IllegalInstantiation.cls.__get__(context.exception, object)
    self.assertIs(cls, THIS)

    with self.assertRaises(IllegalInstantiation) as context:
      _ = OWNER()
    cls = IllegalInstantiation.cls.__get__(context.exception, object)
    self.assertIs(cls, OWNER)

    with self.assertRaises(IllegalInstantiation) as context:
      _ = DESC()
    cls = IllegalInstantiation.cls.__get__(context.exception, object)
    self.assertIs(cls, DESC)

  def test_ad_hoc(self) -> None:
    """
    Ad hoc testing
    """
