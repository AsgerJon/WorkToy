"""
TestAttriBoxInstanceRule subclasses 'DescTest' from the 'tests.test_desc'
package and pins the rule that the value an 'AttriBox' holds is always an
instance of its field type: 'isinstance(foo.bar, Foo.bar.fieldType)'
holds on every read. The rule asks for an instance, not for exactly the
field type, so a 'bool' in an 'int' field and a 'Child' in an
'AttriBox[Parent]' stay as they are. A field type whose constructor
hands back something other than an instance of it is refused with
'TypeException', whether the value is a default or an assignment.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.desc import AttriBox, FixBox
from worktoy.waitaminute import TypeException

from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestAttriBoxInstanceRule(DescTest):
  """
  TestAttriBoxInstanceRule provides tests for the rule that an 'AttriBox'
  always holds an instance of its field type.
  """

  @staticmethod
  def _buildShifty() -> type:
    """The '_buildShifty' method builds a class whose constructor returns
    the 'int' 42 instead of an instance of the class."""

    class Shifty:
      def __new__(cls, *args: Any) -> Any:
        return 42

    return Shifty

  def test_field_object_from_shifty_constructor(self) -> None:
    """This method tests that a field object the constructor returns as
    something other than an instance of the field type does not reach the
    field. Reading it raises 'TypeException' naming the field, the object
    and the field type."""
    shifty = self._buildShifty()

    class Owner:
      field = AttriBox[shifty]()

    with self.assertRaises(TypeException) as context:
      _ = Owner().field
    e = context.exception
    self.assertEqual(e.varName, 'field')
    self.assertEqual(e.actualObject, 42)
    self.assertIn(shifty, e.expectedTypes)

  def test_foreign_object_with_dict_refused(self) -> None:
    """This method tests that a foreign field object with a '__dict__'
    does not reach the field untouched. Reading it raises
    'TypeException'."""

    class Other:
      pass

    class Shifty:
      def __new__(cls, *args: Any) -> Any:
        return Other()

    class Owner:
      field = AttriBox[Shifty]()

    with self.assertRaises(TypeException):
      _ = Owner().field

  def test_assignment_to_shifty_constructor(self) -> None:
    """Assigning a foreign value to such a field raises 'TypeException'
    naming the value: no constructor runs on an assigned value, so the
    constructor never gets to misbehave."""
    shifty = self._buildShifty()

    class Owner:
      field = AttriBox[shifty]()

    with self.assertRaises(TypeException) as context:
      Owner().field = 'anything'
    self.assertEqual(context.exception.actualObject, 'anything')

  def test_constructor_returning_subclass(self) -> None:
    """A constructor that returns an instance of a subclass, as a factory
    might, satisfies the rule, and the field keeps that instance."""

    class Shape:
      def __new__(cls, *args: Any) -> Any:
        return object.__new__(Square)

    class Square(Shape):
      pass

    class Owner:
      shape = AttriBox[Shape]()

    self.assertIs(type(Owner().shape), Square)

  def test_rule_on_ordinary_paths(self) -> None:
    """Defaults, assignments that need a cast and assignments that do not
    all leave the field holding an instance of its field type."""

    class Parent:
      pass

    class Child(Parent):
      pass

    class Text(str):
      pass

    class Owner:
      whole = AttriBox[int](69)
      real = AttriBox[float](1)
      plane = AttriBox[complex](0j)
      text = AttriBox[str]('')
      kin = AttriBox[Parent]()
      fixed = FixBox[float](2)

    owner = Owner()
    reads = [owner.whole, owner.real, owner.fixed]
    owner.whole = 2.0
    owner.real = 2
    owner.plane = 2.0
    owner.text = Text('x')
    owner.kin = Child()
    reads += [owner.whole, owner.real, owner.plane, owner.text, owner.kin]
    names = ['whole', 'real', 'fixed', 'whole', 'real', 'plane', 'text',
             'kin']
    for name, value in zip(names, reads):
      with self.subTest(name=name):
        fieldType = Owner.__dict__[name].fieldType
        self.assertIsInstance(value, fieldType)

  def test_subclass_values_stay(self) -> None:
    """The rule asks for an instance, not for exactly the field type: a
    'bool' in an 'int' field stays a 'bool', and a 'Child' in an
    'AttriBox[Parent]' stays a 'Child'."""

    class Parent:
      pass

    class Child(Parent):
      pass

    class Owner:
      whole = AttriBox[int](True)
      kin = AttriBox[Parent]()

    owner = Owner()
    self.assertIs(owner.whole, True)
    owner.whole = False
    self.assertIs(owner.whole, False)
    child = Child()
    owner.kin = child
    self.assertIs(owner.kin, child)
