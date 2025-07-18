"""
TestAttriBox tests specific functionality of the 'AttriBox' descriptor not
covered by the contextual tests in 'DescTest'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import AttriBox

from . import DescTest

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Dict, Optional


class TestAttriBox(DescTest):
  """
  TestAttriBox tests specific functionality of the 'AttriBox' descriptor not
  covered by the contextual tests in 'DescTest'.
  """

  def test_delete(self) -> None:
    """Test the 'delete' functionality of the 'AttriBox' descriptor."""

    class Foo:
      x = AttriBox[int](0)

    foo = Foo()

    self.assertEqual(foo.x, 0)
    del foo.x

    with self.assertRaises(AttributeError):
      _ = foo.x

    foo.x = 42
    self.assertEqual(foo.x, 42)

    with self.assertRaises(AttributeError):
      del foo.x
      del foo.x  # Second delete should raise an error
