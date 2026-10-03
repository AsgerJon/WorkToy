"""
TestOverloadPlainConflict subclasses 'OverloadTest' and pins that one
class body may not bind a name both to overloads and to a plain
definition. Such a body used to keep one of the two and drop the other
without a word: a plain method won whether it came before or after the
overloads. It now raises 'OverloadConflict' at the second binding, in
either order. A plain definition is any binding that is not an
'overload': a function, a 'property', a 'staticmethod', a constant, or a
value another hook claims, such as an 'EZField'. Overloads at one name
in one body still combine, and so do the bindings of one overload under
two names.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.core.sentinels import ARGS
from worktoy.dispatch import overload
from worktoy.ezdata import EZData, EZField
from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import OverloadConflict

from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestOverloadPlainConflict(OverloadTest):
  """
  TestOverloadPlainConflict provides tests for class bodies binding one
  name both to overloads and to a plain definition.
  """

  def test_plain_then_overload(self) -> None:
    """A plain method followed by an overload of the same name raises,
    naming the class and the name, with the plain definition first."""
    with self.assertRaises(OverloadConflict) as context:
      class Foo(BaseObject):
        def bar(self) -> str:
          return 'plain'  # pragma: no cover

        @overload(int)
        def bar(self, x: int) -> str:
          return 'int'  # pragma: no cover
    e = context.exception
    self.assertEqual(e.className, 'Foo')
    self.assertEqual(e.overloadName, 'bar')
    self.assertFalse(e.overloadsFirst)
    self.assertEqual(str(e), repr(e))
    self.assertEqual(e.msg, str(e))
    self.assertIn("'Foo'", str(e))
    self.assertIn("'bar'", str(e))

  def test_overload_then_plain(self) -> None:
    """An overload followed by a plain method of the same name raises,
    with the overloads first."""
    with self.assertRaises(OverloadConflict) as context:
      class Foo(BaseObject):
        @overload(int)
        def bar(self, x: int) -> str:
          return 'int'  # pragma: no cover

        def bar(self) -> str:
          return 'plain'  # pragma: no cover
    e = context.exception
    self.assertEqual(e.overloadName, 'bar')
    self.assertTrue(e.overloadsFirst)
    self.assertNotEqual(str(e), str(OverloadConflict('Foo', 'bar', False)))

  def test_plain_values_conflict(self) -> None:
    """A 'property', a 'staticmethod' or a constant at the name of an
    overload conflicts as a plain method does, in either order."""

    def makeProperty() -> Any:
      return property(lambda self: 'property')

    def makeStatic() -> Any:
      return staticmethod(lambda: 'static')

    for label, make in (('property', makeProperty),
                        ('staticmethod', makeStatic),
                        ('constant', lambda: 69)):
      with self.subTest(value=label, order='plain first'):
        with self.assertRaises(OverloadConflict):
          class First(BaseObject):
            bar = make()

            @overload(int)
            def bar(self, x: int) -> str:
              return 'int'  # pragma: no cover
      with self.subTest(value=label, order='overload first'):
        with self.assertRaises(OverloadConflict):
          class Second(BaseObject):
            @overload(int)
            def bar(self, x: int) -> str:
              return 'int'  # pragma: no cover

            bar = make()

  def test_fallback_and_finalizer_count(self) -> None:
    """A fallback, a finalizer or a variadic overload counts as an
    overload."""
    with self.assertRaises(OverloadConflict):
      class Fallback(BaseObject):
        @overload.fallback
        def bar(self, *args: Any) -> str:
          return 'fallback'  # pragma: no cover

        bar = 69
    with self.assertRaises(OverloadConflict):
      class Variadic(BaseObject):
        @overload(ARGS[int])
        def bar(self, *args: int) -> str:
          return 'variadic'  # pragma: no cover

        def bar(self) -> str:
          return 'plain'  # pragma: no cover
    with self.assertRaises(OverloadConflict):
      class Finalizer(BaseObject):
        def bar(self) -> str:
          return 'plain'  # pragma: no cover

        @overload.finalize
        def bar(self, *args: Any) -> None:
          pass  # pragma: no cover

  def test_claimed_field_conflicts(self) -> None:
    """An 'EZField', which the EZData hook claims away from the
    namespace, conflicts with an overload of the same name."""
    with self.assertRaises(OverloadConflict):
      class Point(EZData):
        x = EZField[int](0)

        @overload(int)
        def x(self, value: int) -> int:
          return value  # pragma: no cover

  def test_overloads_combine(self) -> None:
    """Overloads at one name combine, the same overload bound again under
    its own name changes nothing, and an overload bound under a second
    name is an alias, not a conflict."""

    class Foo(BaseObject):
      @overload(int)
      def bar(self, x: int) -> str:
        return 'int'

      @overload(str)
      def bar(self, x: str) -> str:
        return 'str'

      bar = bar
      baz = bar

    foo = Foo()
    self.assertEqual(foo.bar(1), 'int')
    self.assertEqual(foo.bar('a'), 'str')
    self.assertEqual(foo.baz(1), 'int')
