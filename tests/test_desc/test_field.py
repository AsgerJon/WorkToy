"""
TestField tests specific functionality of the 'Field' descriptor not
covered by the contextual tests in 'DescTest'.
"""
#  Apache-2.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core import Object
from worktoy.core.sentinels import DELETED
from worktoy.desc import Field
from worktoy.utilities import maybe
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.control_flow import SkipSet
from worktoy.waitaminute.desc import (ProtectedError, ReadOnlyError,
                                      AccessError)
from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import TypeAlias, Union, Optional

  MaybeFloat: TypeAlias = Optional[float]
  FloatField: TypeAlias = Union[float, Field]


class ParentPoint:
  """
  This implementation of the plane point is later subclassed to test
  instantiation of 'Field' descriptors with other 'Field' descriptors as
  argument.
  """

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  NAMESPACE  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  #  Class Variables

  #  Fallback Variables
  __fallback_x__: float = 0
  __fallback_y__: float = 0

  #  Private Variables
  __x_value__: MaybeFloat = None
  __y_value__: MaybeFloat = None

  #  Public Variables
  x: FloatField = Field()
  y: FloatField = Field()

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  GETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  def _createX(self, ) -> None:
    self.__x_value__ = self.__fallback_x__

  def _createY(self, ) -> None:
    self.__y_value__ = self.__fallback_y__

  @x.GET
  def _getX(self, **kwargs) -> float:
    if self.__x_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createX()
      return self._getX(_recursion=True)
    return self.__x_value__

  @y.GET
  def _getY(self, **kwargs) -> float:
    if self.__y_value__ is None:
      if kwargs.get('_recursion', False):
        raise RecursionError
      self._createY()
      return self._getY(_recursion=True)
    return self.__y_value__

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  SETTERS  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @x.SET
  def _setX(self, value: float) -> None:
    self.__x_value__ = value

  @y.SET
  def _setY(self, value: float) -> None:
    self.__y_value__ = value


class TestField(DescTest):
  """
  TestField tests specific functionality of the 'Field' descriptor not
  covered by the contextual tests in 'DescTest'.
  """

  def test_field(self) -> None:
    """Testing the 'Field' descriptor functionality."""

    class DeleteMeNot(Exception):
      pass

    class Secret(Exception):
      pass

    class Foo:
      _x, _y, _z, _v = None, None, None, None

      x = Field()
      y = Field()
      z = Field()
      v = Field()
      w = Field()  # No Access

      @x.GET
      def _getX(self) -> int:
        return maybe(self._x, 0)

      @y.GET
      def _getY(self) -> int:
        if self._y == 'readonly':
          raise ReadOnlyError(self, Foo.y, 'imma write lol!')
        return maybe(self._y, 0)

      @z.GET
      def _getZ(self) -> int:
        return maybe(self._z, 0)

      @z.SET
      def _setZ(self, value: int) -> None:
        self._z = value

      @z.DELETE
      def _delZ(self) -> None:
        raise DeleteMeNot

      @v.GET
      def _getV(self) -> int:
        if self._v == 'raise':
          raise Secret
        return maybe(self._v, 0)

      @v.SET
      def _setV(self, value) -> None:
        self._v = value

      @v.DELETE
      def _deleteV(self) -> None:
        setattr(self, '_v', DELETED)

      def __init__(self, *args) -> None:
        self._x, self._y, self._z, *_ = [*args, None, None, None]

    foo = Foo(69, 420, 0)
    foo.z = 1337
    self.assertEqual(foo.x, 69)
    self.assertEqual(foo.y, 420)
    self.assertEqual(foo.z, 1337)
    bar = Foo()
    self.assertEqual(bar.x, 0)
    self.assertEqual(bar.y, 0)
    self.assertEqual(bar.z, 0)

    with self.assertRaises(AccessError) as context:
      _ = foo.w
    e = context.exception
    self.assertIs(e.desc, Foo.w)
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(ProtectedError) as context:
      del foo.w
    e = context.exception
    self.assertIs(e.instance, foo)
    self.assertIs(e.desc, Foo.w)
    self.assertIsNone(e.oldVal)
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(DeleteMeNot):
      del foo.z

    with self.assertRaises(ProtectedError) as context:
      del foo.x
    e = context.exception
    self.assertIs(e.desc, Foo.x)
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(ReadOnlyError) as context:
      foo.y = 'breh'
    e = context.exception
    self.assertIs(e.desc, Foo.y)
    self.assertEqual(str(e), repr(e))

    with self.assertRaises(AttributeError) as context:
      foo.v = 'lol'
      del foo.v
      del foo.v
    e = context.exception

    with self.assertRaises(AttributeError) as context:
      foo.v = 'lol'
      setattr(foo, '__deleter_keys__', None)
      del foo.v
      del foo.v
    e = context.exception

    with self.assertRaises(Secret) as context:
      foo.v = 'lol'
      setattr(foo, '_v', 'raise')
      del foo.v
    e = context.exception

    with self.assertRaises(ReadOnlyError) as context:
      setattr(foo, '__delete_keys__', None)
      setattr(foo, '_y', 'readonly')
      del foo.y
    e = context.exception
    self.assertIs(e.instance, foo)
    self.assertIs(e.desc, Foo.y)
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.newVal, 'imma write lol!', )

  def test_bad_delete(self) -> None:
    """Testing that 'Field' raises 'AttributeError' when delete fails."""

    class Foo69420:
      __x_fallback__ = 0
      __x_value__ = None
      x = Field()

      @x.GET
      def _getX(self) -> int:
        if self.__x_value__ is DELETED:
          raise AttributeError('x')
        return maybe(self.__x_value__, self.__x_fallback__)

      @x.SET
      def _setX(self, value) -> None:
        self.__x_value__ = value

      def __init__(self, *args) -> None:
        self.x = (*args, self.__x_fallback__)[0]

    foo = Foo69420()
    with self.assertRaises(ProtectedError) as context:
      del foo.x
    e = context.exception
    self.assertIs(e.instance, foo)
    self.assertIs(e.desc, Foo69420.x)
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.oldVal, 0)

    setattr(foo, '__x_value__', DELETED)

    #  Here, during the failing 'deletion', the 'oldVal' is set to 'None'
    with self.assertRaises(ProtectedError) as context:
      del foo.x
    e = context.exception
    self.assertIs(e.instance, foo)
    self.assertIs(e.desc, Foo69420.x)
    self.assertEqual(str(e), repr(e))
    self.assertIsNone(e.oldVal)

  def test_init_bad(self, ) -> None:
    """
    This method tests the error raised when constructing a 'Field' with an
    unsupported argument. Only 'None' and 'Field' are supported.
    """
    with self.assertRaises(TypeException) as context:
      _ = Field(69)
    e = context.exception
    self.assertEqual(e.varName, 'other')
    self.assertEqual(e.actualObject, 69)
    self.assertIs(e.actualType, int)
    self.assertIn(Field, e.expectedTypes)

  def test_init(self, ) -> None:
    """
    This method tests the construction of 'Field' instances with valid
    arguments.
    """

    class ChildPoint(ParentPoint):
      x = Field(ParentPoint.x)
      y = Field(ParentPoint.y)

      @x.preSet
      def _preSetX(self, value: float) -> None:
        cls = type(self)
        fieldObject = getattr(cls, 'x')
        if not isinstance(value, (int, float)):
          raise TypeException('value', value, float)
        getKey = object.__getattribute__(fieldObject, '__get_key__')
        getterFunc = getattr(cls, getKey)
        try:
          existing = getterFunc(self, _recursion=True)
        except RecursionError:
          return
        else:
          if abs(existing - value) < 1e-16:
            raise SkipSet

      @y.preSet
      def _preSetY(self, value: float) -> None:
        cls = type(self)
        fieldObject = getattr(cls, 'y')
        if not isinstance(value, (int, float)):
          raise TypeException('value', value, float)
        getKey = object.__getattribute__(fieldObject, '__get_key__')
        getterFunc = getattr(cls, getKey)
        try:
          existing = getterFunc(self, _recursion=True)
        except RecursionError:
          return
        else:
          if abs(existing - value) < 1e-16:
            raise SkipSet

    childPoint = ChildPoint()
    parentPoint = ParentPoint()
    expectedX = ChildPoint.__fallback_x__
    expectedY = ChildPoint.__fallback_y__
    self.assertEqual(parentPoint.x, expectedX)
    self.assertEqual(parentPoint.y, expectedY)
    with self.assertRaises(TypeException) as context:
      childPoint.x = 'sixty-nine'  # type: ignore[assignment]
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertEqual(e.actualObject, 'sixty-nine')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)
    with self.assertRaises(TypeException) as context:
      childPoint.y = 'four-twenty'  # type: ignore[assignment]
    e = context.exception
    self.assertEqual(e.varName, 'value')
    self.assertEqual(e.actualObject, 'four-twenty')
    self.assertIs(e.actualType, str)
    self.assertIn(float, e.expectedTypes)

    #  The following two should be skipped by the 'SkipSet' raised in
    #  their 'preSet' hooks.
    childPoint.x = expectedX
    childPoint.y = expectedY
    self.assertEqual(childPoint.x, expectedX)
    self.assertEqual(childPoint.y, expectedY)
    #  Do it again to cover 'SkipSet' handling.
    childPoint.x = expectedX
    childPoint.y = expectedY
    self.assertEqual(childPoint.x, expectedX)
    self.assertEqual(childPoint.y, expectedY)
    #  And again, to set an actually different value, which should not be
    #  skipped.
    childPoint.x = expectedX + 1
    childPoint.y = expectedY + 1
    self.assertEqual(childPoint.x, expectedX + 1)
    self.assertEqual(childPoint.y, expectedY + 1)

  def test_bad_key_type(self, ) -> None:
    """
    This method tests the '__get_key__' attribute to be of the wrong type.
    """

    class Sus(Object):
      tom: Field[str] = Field()
      dick: Field[str] = Field()
      harry: Field[str] = Field()

      @tom.GET
      def _getTom(self) -> int:
        return 69420

    sus = Sus()

    setattr(Sus.harry, '__get_key__', sus.tom)

    self.assertEqual(sus.tom, 69420)

    with self.assertRaises(AccessError) as context:
      _ = sus.dick
    e = context.exception
    self.assertIs(e.desc, Sus.dick)

    with self.assertRaises(TypeException) as context:
      _ = sus.harry
    e = context.exception
    self.assertEqual(e.varName, '__get_key__')
    self.assertEqual(e.actualObject, sus.tom)
    self.assertIs(e.actualType, int)
    self.assertIn(str, e.expectedTypes)
