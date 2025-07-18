"""
TestField tests specific functionality of the 'Field' descriptor not
covered by the contextual tests in 'DescTest'.
"""
#  AGPL-3.0 license
#  Copyright (c) 2025 Asger Jon Vistisen
from __future__ import annotations

from tests import WYD
from worktoy.core.sentinels import DELETED
from worktoy.desc import Field
from worktoy.utilities import maybe
from worktoy.waitaminute.desc import ProtectedError, ReadOnlyError, \
  AccessError

from . import DescTest

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any, Dict, Optional


class TestField(DescTest):
  """
  TestField tests specific functionality of the 'Field' descriptor not
  covered by the contextual tests in 'DescTest'.
  """

  def test_field(self) -> None:
    """Test the 'Field' descriptor functionality."""

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
        raise WYD

      @v.GET
      def _getV(self) -> int:
        if self._v == 'raise':
          raise WYD
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

    with self.assertRaises(AttributeError) as context:
      del foo.w
    e = context.exception
    self.assertIsInstance(e.__cause__, AccessError)

    with self.assertRaises(WYD):
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

    with self.assertRaises(WYD) as context:
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
