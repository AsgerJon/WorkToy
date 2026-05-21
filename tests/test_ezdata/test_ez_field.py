"""
TestEZField subclasses 'EZTest' from the 'tests.test_ezdata' package and
provides tests for the 'EZField' class from the 'worktoy.ezdata' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZField, EZData
from worktoy.waitaminute import MissingVariable, TypeException
from . import EZTest
from .examples import FullName, Point2D, Circle

if TYPE_CHECKING:  # pragma: no cover
  pass
else:
  NotImpType = type(NotImplemented)


class TestEZField(EZTest):
  """
  TestEZField subclasses 'EZTest' from the 'tests.test_ezdata' package and
  provides tests for the 'EZField' class from the 'worktoy.ezdata' package.
  """

  def test_missing_field_owner(self) -> None:
    """
    This method tests the branch where the '__field_owner__' attribute has
    not been set.
    """
    f = EZField[int](0)
    with self.assertRaises(MissingVariable) as context:
      _ = f._getFieldOwner()
    e = context.exception
    self.assertIs(e.instance, f)
    self.assertEqual(e.varName, '__field_owner__')
    self.assertIn(type, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_missing_field_name(self) -> None:
    """
    This method tests the branch where the '__field_name__' attribute has not
    been set.
    """
    f = EZField[int](0)
    with self.assertRaises(MissingVariable) as context:
      _ = f._getFieldName()
    e = context.exception
    self.assertIs(e.instance, f)
    self.assertEqual(e.varName, '__field_name__')
    self.assertIn(str, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_missing_field_type(self) -> None:
    """
    This method tests the branch where the '__field_type__' attribute has not
    been set.
    """
    f = EZField[int]
    object.__delattr__(f, '__field_type__')
    with self.assertRaises(MissingVariable) as context:
      _ = f._getFieldType()  # type: ignore
    e = context.exception
    self.assertIs(e.instance, f)
    self.assertEqual(e.varName, '__field_type__')
    self.assertIn(type, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_bad_type_field_owner(self) -> None:
    """
    This method tests the branch where the '__field_owner__' attribute is
    not a 'type' object.
    """
    f = EZField[int](0)
    # noinspection PyTypeChecker
    f.__field_owner__ = 0
    with self.assertRaises(TypeException) as context:
      _ = f._getFieldOwner()
    e = context.exception
    self.assertEqual(e.varName, '__field_owner__')
    self.assertEqual(e.actualObject, 0)
    self.assertEqual(e.actualType, int)
    self.assertIn(type, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_bad_type_field_name(self) -> None:
    """
    This method tests the branch where the '__field_name__' attribute is
    not a 'str' object.
    """
    f = EZField[int](0)
    # noinspection PyTypeChecker
    f.__field_name__ = 0
    with self.assertRaises(TypeException) as context:
      _ = f._getFieldName()
    e = context.exception
    self.assertEqual(e.varName, '__field_name__')
    self.assertEqual(e.actualObject, 0)
    self.assertEqual(e.actualType, int)
    self.assertIn(str, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_bad_type_field_type(self) -> None:
    """
    This method tests the branch where the '__field_type__' attribute is
    not a 'type' object.
    """
    f = EZField[int]
    # noinspection PyTypeChecker
    f.__field_type__ = 0
    with self.assertRaises(TypeException) as context:
      _ = f._getFieldType()  # type: ignore
    e = context.exception
    self.assertEqual(e.varName, '__field_type__')
    self.assertEqual(e.actualObject, 0)
    self.assertEqual(e.actualType, int)
    self.assertIn(type, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_missing_pos_args(self) -> None:
    """
    This method tests the branch where the '__pos_args__' attribute has not
    been set.
    """
    f = EZField[int](0)
    object.__setattr__(f, '__pos_args__', None)
    with self.assertRaises(MissingVariable) as context:
      _ = f._getPosArgs()
    e = context.exception
    self.assertIs(e.instance, f)
    self.assertEqual(e.varName, '__pos_args__')
    self.assertIn(tuple, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_bad_type_pos_args(self) -> None:
    """
    This method tests the branch where the '__pos_args__' attribute is not a
    'tuple' object.
    """
    f = EZField[int](0)
    # noinspection PyTypeChecker
    f.__pos_args__ = 0
    with self.assertRaises(TypeException) as context:
      _ = f._getPosArgs()
    e = context.exception
    self.assertEqual(e.varName, '__pos_args__')
    self.assertEqual(e.actualObject, 0)
    self.assertEqual(e.actualType, int)
    self.assertIn(tuple, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_missing_key_args(self) -> None:
    """
    This method tests the branch where the '__key_args__' attribute has not
    been set.
    """
    f = EZField[int](0)
    object.__setattr__(f, '__key_args__', None)
    with self.assertRaises(MissingVariable) as context:
      _ = f._getKeyArgs()
    e = context.exception
    self.assertIs(e.instance, f)
    self.assertEqual(e.varName, '__key_args__')
    self.assertIn(dict, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_bad_type_key_args(self) -> None:
    """
    This method tests the branch where the '__key_args__' attribute is not a
    'dict' object.
    """
    f = EZField[int](0)
    # noinspection PyTypeChecker
    f.__key_args__ = 0
    with self.assertRaises(TypeException) as context:
      _ = f._getKeyArgs()
    e = context.exception
    self.assertEqual(e.varName, '__key_args__')
    self.assertEqual(e.actualObject, 0)
    self.assertEqual(e.actualType, int)
    self.assertIn(dict, e.expectedTypes)
    self.assertEqual(str(e), repr(e))

  def test_str_repr(self, ) -> None:
    """
    This method tests the '__str__' and '__repr__' methods.
    """

    class Foo(EZData):
      z = EZField[complex](69, 420)
      name = EZField[FullName]('Doe', givenName='John')
      bar = EZField[str]()
      circle = EZField[Circle](center=Point2D(69, 420), radius=1337)

    expectedStr = """Foo.z: complex(69, 420)"""
    actualStr = str(Foo.__ez_fields__['z'])
    self.assertEqual(expectedStr, actualStr)

    expectedRepr = """EZField[complex](69, 420)"""
    actualRepr = repr(Foo.__ez_fields__['z'])
    self.assertEqual(expectedRepr, actualRepr)

    expectedStr = """Foo.name: FullName('Doe', givenName='John')"""
    actualStr = str(Foo.__ez_fields__['name'])
    self.assertEqual(expectedStr, actualStr)

    expectedRepr = """EZField[FullName]('Doe', givenName='John')"""
    actualRepr = repr(Foo.__ez_fields__['name'])
    self.assertEqual(expectedRepr, actualRepr)

    expectedStr = """Foo.bar: str()"""
    actualStr = str(Foo.__ez_fields__['bar'])
    self.assertEqual(expectedStr, actualStr)

    expectedRepr = """EZField[str]()"""
    actualRepr = repr(Foo.__ez_fields__['bar'])
    self.assertEqual(expectedRepr, actualRepr)

    expectedParts = (
      """Foo.circle: """,
      """Circle(""",
      """center=Point2D(""",
      """radius=1337""",
    )
    actualStr = str(Foo.__ez_fields__['circle'])
    for part in expectedParts:
      self.assertIn(part, actualStr)

    expectedParts = (
      """EZField[Circle](""",
      """center=Point2D(""",
      """radius=1337""",
    )
    actualRepr = repr(Foo.__ez_fields__['circle'])
    for part in expectedParts:
      self.assertIn(part, actualRepr)

  def test_str_on_unbound_does_not_raise(self) -> None:
    """
    'str' on an EZField that has not yet been bound to an EZData
    class returns a string rather than raising, matching the
    defensive behavior of '__repr__'. The placeholders make the
    unbound state visible without leaking 'MissingVariable'.
    """
    f = EZField[float](0.0)
    text = str(f)
    self.assertIsInstance(text, str)
    self.assertIn('<unbound>', text)
    self.assertIn('float', text)
