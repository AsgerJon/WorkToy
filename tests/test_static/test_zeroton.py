"""TestZeroton tests the Zeroton metaclass. """
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.static import Zeroton, THIS, OWNER, ATTR
from worktoy.waitaminute import IllegalInstantiationError

try:
  from typing import TYPE_CHECKING
except ImportError:
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
    self.assertIsInstance(ATTR, Zeroton)

  def test_raises(self, ) -> None:
    """Test that the Zeroton metaclass raises the correct exceptions."""
    with self.assertRaises(IllegalInstantiationError) as context:
      _ = THIS()
    cls = IllegalInstantiationError.cls.__get__(context.exception, object)
    self.assertIs(cls, THIS)

    with self.assertRaises(IllegalInstantiationError) as context:
      _ = OWNER()
    cls = IllegalInstantiationError.cls.__get__(context.exception, object)
    self.assertIs(cls, OWNER)

    with self.assertRaises(IllegalInstantiationError) as context:
      _ = ATTR()
    cls = IllegalInstantiationError.cls.__get__(context.exception, object)
    self.assertIs(cls, ATTR)
