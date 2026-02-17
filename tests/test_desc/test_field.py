"""
TestField tests specific functionality of the 'Field' descriptor not
covered by the contextual tests in 'DescTest'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025-2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import DELETED
from worktoy.desc import Field
from worktoy.utilities import maybe
from worktoy.waitaminute.desc import ProtectedError, ReadOnlyError, \
  AccessError
from . import DescTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestField(DescTest):
  """
  TestField tests specific functionality of the 'Field' descriptor not
  covered by the contextual tests in 'DescTest'.
  """

  def test_field(self) -> None:
    """Test the 'Field' descriptor functionality."""

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
    """Test that 'Field' raises 'AttributeError' when delete fails."""

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
