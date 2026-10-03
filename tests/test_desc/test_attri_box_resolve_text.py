"""
TestAttriBoxResolveText subclasses 'DescTest' from the 'tests.test_desc'
package and pins 'AttriBox.resolveText' as the place a box decides how a
single value becomes the value of a text field. A subclass replacing it
changes the policy for every text field of that box class, by default and
by assignment, while the rule that a field holds an instance of its field
type still applies to what it returns. Field types that are not text
never reach it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox
from worktoy.waitaminute import TypeException

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestAttriBoxResolveText(DescTest):
  """
  TestAttriBoxResolveText provides tests for subclasses of 'AttriBox'
  replacing 'resolveText'.
  """

  def test_lenient_subclass(self) -> None:
    """A subclass calling the constructor instead accepts anything again,
    by default and by assignment."""

    class LooseBox(AttriBox):
      def resolveText(self, value: Any) -> Any:
        return self.getFieldType()(value)

    class Foo:
      name = LooseBox[str](5)

    foo = Foo()
    self.assertEqual(foo.name, '5')
    foo.name = None
    self.assertEqual(foo.name, 'None')

  def test_receives_the_value(self) -> None:
    """The method receives the single value, for the default and for an
    assignment, and only for a text field."""
    seen = []

    class SpyBox(AttriBox):
      def resolveText(self, value: Any) -> Any:
        seen.append(value)
        return AttriBox.resolveText(self, value)

    class Foo:
      name = SpyBox[str](b'abc')
      count = SpyBox[int](3)

    foo = Foo()
    self.assertEqual(foo.name, 'abc')
    foo.name = bytearray(b'xyz')
    self.assertEqual(foo.count, 3)
    foo.count = 4.0
    self.assertEqual(seen, [b'abc', bytearray(b'xyz')])

  def test_text_subclass_field(self) -> None:
    """A field type based on a text type, such as a subclass of 'str',
    counts as a text field and reaches the method too."""
    seen = []

    class Label(str):
      pass

    class SpyBox(AttriBox):
      def resolveText(self, value: Any) -> Any:
        seen.append(value)
        return Label('spied')

    class Foo:
      label = SpyBox[Label](5)

    self.assertEqual(Foo().label, 'spied')
    self.assertEqual(seen, [5])

  def test_instance_rule_still_applies(self) -> None:
    """A replacement returning something that is not an instance of the
    field type is refused with 'TypeException'."""

    class WrongBox(AttriBox):
      def resolveText(self, value: Any) -> Any:
        return 42

    class Foo:
      name = WrongBox[str](b'abc')

    with self.assertRaises(TypeException):
      _ = Foo().name
