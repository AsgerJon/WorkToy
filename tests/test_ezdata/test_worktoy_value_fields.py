"""
TestWorktoyValueFields subclasses 'EZTest' from the 'tests.test_ezdata'
package and pins which class-body values of an EZData class become fields.
A bare value becomes a field, and a descriptor stays a class attribute.
'EZHook' used to count as a descriptor any value whose type defines
'__get__', '__set__', '__delete__' or '__set_name__', and every object
deriving from 'Object' defines all four, so an enumeration member, an
EZData instance or a 'SymbolicName' in a class body was left out of the
fields. Now a value that is not an 'Object' is a descriptor when its type
implements '__get__' or '__set__', and an 'Object' is one when its type
overrides '__instance_get__' or '__instance_set__', where every 'Object'
descriptor does its work.

A field default is built by calling the field type with the declared
arguments, and for a lone argument already of the field type that call is
no copy: 'Point(Point(1, 2))' failed on every construction, and
'SymbolicName' nested one name in another. Such an argument is now copied,
so each instance still receives an object of its own.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object
from worktoy.desc import Field, SymbolicName
from worktoy.ezdata import EZData, EZField
from worktoy.keenum import KeeNum, Kee

from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class Color(KeeNum):
  """Color provides the members used as values below."""

  RED = Kee[str]('red')
  BLUE = Kee[str]('blue')


class Point(EZData):
  """Point is the EZData class used as a value below."""

  x = EZField[int](0)
  y = EZField[int](0)


class Plain:
  """Plain is a descriptor that does not derive from 'Object'."""

  def __get__(self, instance: Any, owner: type) -> Any:
    return 'plain'


class SetOnly:
  """SetOnly is a descriptor with '__set__' alone, not an 'Object'."""

  def __set__(self, instance: Any, value: Any) -> None:
    instance.__dict__['_setOnly'] = value


class GetOnly(Object):
  """GetOnly is an 'Object' overriding '__instance_get__' alone."""

  def __instance_get__(self, instance: Any, owner: type, **kwargs) -> Any:
    return 'got'


class SetterOnly(Object):
  """SetterOnly is an 'Object' overriding '__instance_set__' alone."""

  def __instance_set__(self, instance: Any, value: Any, **kwargs) -> None:
    object.__setattr__(instance, '_setterOnly', value)


class Car(EZData):
  """Car holds a member, an EZData instance and a name as bare values,
  beside descriptors that stay class attributes."""

  color = Color.RED
  origin = Point(1, 2)
  label = SymbolicName('a', 'b')
  wheels = 4
  plain = Plain()
  setOnly = SetOnly()
  getOnly = GetOnly()
  setterOnly = SetterOnly()
  doubled = Field()

  @doubled.GET
  def _getDoubled(self) -> int:
    return self.wheels * 2

  @property
  def described(self) -> str:
    return '%s car' % self.color.name.lower()


class Explicit(EZData):
  """Explicit declares the same kinds of value through 'EZField'."""

  origin = EZField[Point](Point(3, 4))
  items = EZField[list]([1, 2])


class TestWorktoyValueFields(EZTest):
  """
  TestWorktoyValueFields provides tests for class-body values that are
  worktoy objects.
  """

  def test_values_become_fields(self) -> None:
    """A member, an EZData instance and a name become fields, in the
    order of the class body."""
    names = [field.fieldName for field in Car.fields]
    self.assertEqual(names, ['color', 'origin', 'label', 'wheels'])

  def test_defaults(self) -> None:
    """Each value is the default of its field."""
    car = Car()
    self.assertIs(car.color, Color.RED)
    self.assertEqual(car.origin, Point(1, 2))
    self.assertEqual(car.label.words, ('a', 'b'))
    self.assertEqual(car.wheels, 4)

  def test_positional_arguments(self) -> None:
    """The fields take positional arguments like any other field."""
    car = Car(Color.BLUE, Point(5, 6), SymbolicName('c'), 3)
    self.assertIs(car.color, Color.BLUE)
    self.assertEqual(car.origin, Point(5, 6))
    self.assertEqual(car.label.words, ('c',))
    self.assertEqual(car.wheels, 3)

  def test_default_copied_per_instance(self) -> None:
    """Each instance receives a copy of the default of its own."""
    first, second = Car(), Car()
    self.assertIsNot(first.origin, second.origin)
    self.assertIsNot(first.origin, Car.fields[1].posArgs[0])
    self.assertIs(first.color, second.color)

  def test_descriptors_stay_attributes(self) -> None:
    """A descriptor not deriving from 'Object', a 'Field' and a
    'property' stay class attributes and work as such."""
    car = Car()
    self.assertEqual(car.plain, 'plain')
    self.assertEqual(car.doubled, 8)
    self.assertEqual(car.described, 'red car')

  def test_explicit_field_of_instance(self) -> None:
    """An explicit 'EZField' whose lone argument is of its field type
    copies it rather than calling the field type on it."""
    first, second = Explicit(), Explicit()
    self.assertEqual(first.origin, Point(3, 4))
    self.assertIsNot(first.origin, second.origin)

  def test_builtin_default_unchanged(self) -> None:
    """A builtin default is still a fresh equal object per instance."""
    first, second = Explicit(), Explicit()
    self.assertEqual(first.items, [1, 2])
    self.assertIsNot(first.items, second.items)

  def test_one_sided_descriptors_stay_attributes(self) -> None:
    """A descriptor implementing one side only stays a class attribute:
    '__set__' alone outside 'Object', and '__instance_get__' or
    '__instance_set__' alone on an 'Object'."""
    car = Car()
    car.setOnly = 1
    car.setterOnly = 2
    self.assertEqual(car.__dict__['_setOnly'], 1)
    self.assertEqual(car.__dict__['_setterOnly'], 2)
    self.assertEqual(car.getOnly, 'got')
