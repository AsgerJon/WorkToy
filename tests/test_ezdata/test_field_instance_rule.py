"""
TestFieldInstanceRule subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins the rule that every field of an 'EZData' instance holds
an instance of its field type, as an 'AttriBox' does. The rule asks for
an instance, not for exactly the field type, so a 'bool' in an 'int'
field and a 'Child' in a 'Parent' field stay as they are. A field type
whose constructor hands back something other than an instance of it is
refused with 'TypeException' wherever EZData calls it: building a
default, casting a constructor argument, casting an assignment, and the
'defaultValue' of the field.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField
from worktoy.waitaminute import TypeException

from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestFieldInstanceRule(EZTest):
  """
  TestFieldInstanceRule provides tests for the rule that an 'EZData'
  field always holds an instance of its field type.
  """

  @staticmethod
  def _buildShifty() -> type:
    """The '_buildShifty' method builds a class whose constructor returns
    the 'int' 42 instead of an instance of the class."""

    class Shifty:
      def __new__(cls, *args: Any) -> Any:
        return 42

    return Shifty

  def test_default_from_shifty_constructor(self) -> None:
    """Building the default of such a field raises 'TypeException',
    naming the field, the value and the field type."""
    shifty = self._buildShifty()

    class Holder(EZData):
      odd = EZField[shifty]()

    with self.assertRaises(TypeException) as context:
      Holder()
    e = context.exception
    self.assertEqual(e.varName, 'odd')
    self.assertEqual(e.actualObject, 42)
    self.assertIn(shifty, e.expectedTypes)

  def test_argument_to_shifty_constructor(self) -> None:
    """A constructor argument cast through such a field type raises
    'TypeException', naming the argument."""
    shifty = self._buildShifty()

    class Holder(EZData):
      odd = EZField[shifty]()
      whole = EZField[int](0)

    with self.assertRaises(TypeException) as context:
      Holder(odd='x')
    self.assertEqual(context.exception.actualObject, 'x')

  def test_assignment_to_shifty_constructor(self) -> None:
    """Assigning to such a field raises 'TypeException', as long as
    building the instance got that far."""
    shifty = self._buildShifty()

    class Holder(EZData):
      odd = EZField[shifty]()

    holder = Holder.__new__(Holder)
    with self.assertRaises(TypeException) as context:
      holder.odd = 'x'
    self.assertEqual(context.exception.actualObject, 'x')

  def test_default_value_of_shifty_field(self) -> None:
    """The 'defaultValue' of such a field raises 'TypeException' rather
    than returning what the constructor returned."""
    shifty = self._buildShifty()
    with self.assertRaises(TypeException) as context:
      _ = EZField[shifty]().defaultValue
    self.assertEqual(context.exception.actualObject, 42)

  def test_constructor_returning_subclass(self) -> None:
    """A default whose constructor returns an instance of a subclass, as
    a factory might, satisfies the rule and is kept."""

    class Shape:
      def __new__(cls, *args: Any) -> Any:
        return object.__new__(Square)

    class Square(Shape):
      pass

    class Holder(EZData):
      shape = EZField[Shape]()

    self.assertIs(type(Holder().shape), Square)
    self.assertIs(type(Holder.__ez_fields__['shape'].defaultValue), Square)

  def test_subclass_values_stay(self) -> None:
    """A 'bool' in an 'int' field stays a 'bool' and a 'Child' in a
    'Parent' field stays a 'Child', given by construction or by
    assignment."""

    class Parent:
      pass

    class Child(Parent):
      pass

    class Holder(EZData):
      whole = EZField[int](0)
      kin = EZField[Parent]()

    child = Child()
    holder = Holder(True, child)
    self.assertIs(holder.whole, True)
    self.assertIs(holder.kin, child)
    holder.whole = False
    self.assertIs(holder.whole, False)

  def test_rule_on_ordinary_paths(self) -> None:
    """Defaults, constructor arguments and assignments that need a cast
    all leave each field holding an instance of its field type."""

    class Holder(EZData):
      real = EZField[float](1)
      plane = EZField[complex](0)
      text = EZField[str]('')

    for holder in (Holder(), Holder(2, 2.0, b'bytes')):
      for field in Holder.fields:
        with self.subTest(field=field.fieldName):
          value = getattr(holder, field.fieldName)
          self.assertIsInstance(value, field.fieldType)
    holder = Holder()
    holder.real = 3
    self.assertIsInstance(holder.real, float)
