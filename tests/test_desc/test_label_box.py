"""
TestLabelBox provides unit tests specifically for the `LabelBox` descriptor.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import LabelBox
from worktoy.waitaminute import WriteOnceError
from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestLabelBox(DescTest):
  """
  TestLabelBox provides unit tests specifically for the `LabelBox`
  descriptor.
  """

  def test_label_box(self) -> None:
    """Test the functionality of the LabelBox descriptor."""

    class Foo:
      bar = LabelBox[int](0)

    foo = Foo()
    self.assertEqual(foo.bar, 0)
    with self.assertRaises(WriteOnceError) as context:
      foo.bar = 42
    e = context.exception
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.oldValue, 0)
    self.assertEqual(e.newValue, 42)
    self.assertEqual(e.desc, Foo.bar)
    del foo.bar
    with self.assertRaises(AttributeError):
      _ = foo.bar  # Should raise an error since it was deleted
    with self.assertRaises(AttributeError):
      del foo.bar  # Second delete should raise an error
    foo.bar = 69
    self.assertEqual(foo.bar, 69)
