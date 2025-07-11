"""
TestLabelBox tests the LabelBox class from the worktoy.desc module.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core import Object
from worktoy.desc import LabelBox
from worktoy.waitaminute import WriteOnceError
from . import DescTest

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Type


class Foo(Object):
  """Foo is a simple class for testing purposes."""

  bar = LabelBox[int](69)


class TestLabelBox(DescTest):
  """
  TestLabelBox tests the LabelBox class from the worktoy.desc module.
  """

  def test_label_box(self) -> None:
    foo = Foo()

    with self.assertRaises(WriteOnceError) as context:
      foo.bar = 69
      foo.bar = 420

  def test_label_box_delete(self) -> None:
    foo = Foo()
    foo.bar = 1337

    self.assertEqual(foo.bar, 1337)
    del foo.bar
    with self.assertRaises(AttributeError):
      _ = foo.bar
    with self.assertRaises(AttributeError):
      del foo.bar

    foo.bar = 80085
    self.assertEqual(foo.bar, 80085)

    del foo.bar

    foo.bar = 69.0
    self.assertEqual(foo.bar, 69)
