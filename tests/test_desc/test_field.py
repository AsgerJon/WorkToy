"""
TestField tests 'Field' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.desc import Field, AttriBox
from worktoy.dispatch import isFlex
from worktoy.waitaminute import MissingVariable, TypeException
from worktoy.waitaminute.desc import AccessError, ReadOnlyError
from worktoy.waitaminute.desc import ProtectedError
from . import DescTest, Circle


class TestField(DescTest):
  """
  A 'Field' computes or guards an attribute through methods the class
  marks as its getter, setters and deleters, found by name at each
  access so a subclass may override them. The tests pin the three
  accesses, the refusals without a getter, setter or deleter, the
  override, the kinds a getter may be, the value a deletion reports
  when the getter raises, the copy constructor and the checked key.
  """

  def test_read_write_delete(self) -> None:
    circle = Circle()
    self.assertEqual(circle.radius, 1.0)
    circle.radius = 2.0
    self.assertEqual(circle.store, 2.0)
    self.assertEqual(circle.written, [2.0])
    self.assertEqual(circle.area, 12.0)
    del circle.radius
    with self.assertRaises(MissingVariable) as context:
      _ = circle.radius
    self.assertEqual(context.exception.varName, 'store')
    self.assertIs(context.exception.instance, circle)
    self.assertEqual(context.exception.expectedTypes, (object,))
    self.assertEqual(str(context.exception),
                     "Missing 'Circle.store: object'!")
    self.assertIsInstance(Circle.radius, Field)

  def test_decorators_return_method_unchanged(self) -> None:
    self.assertFalse(isFlex(Circle.__dict__['_getRadius']))
    self.assertEqual(Circle.__dict__['radius']._getSetterKeys(),
                     ('_setRadius', '_noteRadius'))
    self.assertEqual(Circle.__dict__['radius']._getDeleterKeys(),
                     ('_delRadius',))
    self.assertEqual(Circle.__dict__['area']._getSetterKeys(), ())

  def test_no_getter(self) -> None:
    class Owner:
      f = Field()

    with self.assertRaises(AccessError) as context:
      _ = Owner().f
    self.assertIs(context.exception.desc, Owner.__dict__['f'])
    self.assertIn("The 'Field' descriptor at 'Owner.f'",
                  str(context.exception))
    self.assertFalse(hasattr(Owner(), 'f'))

  def test_no_setter(self) -> None:
    circle = Circle()
    with self.assertRaises(ReadOnlyError) as context:
      circle.area = 5.0
    self.assertIs(context.exception.desc, Circle.__dict__['area'])
    self.assertIs(context.exception.instance, circle)
    self.assertEqual(context.exception.newVal, 5.0)
    self.assertIn("'Circle.area'", str(context.exception))
    self.assertIn("'5.0'", str(context.exception))

  def test_no_deleter_reports_old_value(self) -> None:
    circle = Circle()
    with self.assertRaises(ProtectedError) as context:
      del circle.area
    self.assertEqual(context.exception.oldVal, 3.0)
    self.assertIs(context.exception.instance, circle)
    self.assertIs(context.exception.desc, Circle.__dict__['area'])
    self.assertIn("'Circle.area'", str(context.exception))
    self.assertIn("'3.0'", str(context.exception))

  def test_deletion_survives_a_raising_getter(self) -> None:
    class Owner:
      f = Field()

      @f.GET
      def _getF(self) -> None:
        raise ValueError('not ready')

    with self.assertRaises(ProtectedError) as context:
      del Owner().f
    self.assertIsNone(context.exception.oldVal)
    self.assertIs(context.exception.desc, Owner.__dict__['f'])
    self.assertIsInstance(context.exception.instance, Owner)
    self.assertIn("'Owner.f'", str(context.exception))
    self.assertIn("'None'", str(context.exception))
    with self.assertRaises(ValueError) as context:
      _ = Owner().f
    self.assertEqual(str(context.exception), 'not ready')

  def test_override_in_subclass(self) -> None:
    class Wide(Circle):
      def _getRadius(self) -> float:
        return self.store * 10

    wide = Wide()
    self.assertEqual(wide.radius, 10.0)
    self.assertEqual(wide.area, 300.0)

  def test_getter_kinds(self) -> None:
    class Owner:
      classy = Field()
      static = Field()

      @classy.GET
      @classmethod
      def _getClassy(cls) -> str:
        return cls.__name__

      @static.GET
      @staticmethod
      def _getStatic() -> str:
        return 'static'

    self.assertEqual(Owner().classy, 'Owner')
    self.assertEqual(Owner().static, 'static')

  def test_copy_constructor(self) -> None:
    original = Circle.__dict__['radius']
    copy = Field(original)
    self.assertEqual(copy._getGetterKey(), '_getRadius')
    self.assertEqual(copy._getSetterKeys(), original._getSetterKeys())
    self.assertEqual(copy._getDeleterKeys(), original._getDeleterKeys())
    self.assertIsNone(copy.getFieldOwner())
    blank = Field(Field())
    with self.assertRaises(AccessError) as context:
      blank._getGetterKey()
    self.assertIs(context.exception.desc, blank)
    self.assertIn("'Field' descriptor at 'object.object'",
                  str(context.exception))
    with self.assertRaises(TypeException) as context:
      Field(5)
    self.assertEqual(context.exception.varName, 'other')
    self.assertEqual(context.exception.actualObject, 5)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (Field,))
    self.assertIn("'other'", str(context.exception))

  def test_getter_key_checked(self) -> None:
    field = Field()
    object.__setattr__(field, '__get_key__', 42)
    with self.assertRaises(TypeException) as context:
      field._getGetterKey()
    self.assertEqual(context.exception.varName, '__get_key__')
    self.assertEqual(context.exception.actualObject, 42)
    self.assertIs(context.exception.actualType, int)
    self.assertEqual(context.exception.expectedTypes, (str,))
    self.assertIn("'__get_key__'", str(context.exception))

  def test_random_radii(self) -> None:
    circle = Circle()
    for value in self.randomFloat.row:
      circle.radius = value
      with self.subTest(value=value):
        self.assertEqual(circle.radius, value)
        self.assertEqual(circle.area, 3.0 * value * value)
