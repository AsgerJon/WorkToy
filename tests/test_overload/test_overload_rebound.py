"""
TestOverloadRebound subclasses 'OverloadTest' and pins that one 'overload'
object bound in the bodies of two classes builds a 'Dispatcher' in each,
whatever name each binds it to. The name a class body claimed an overload
under used to be written on the overload object itself, where it outlived
the class body, so a second class binding the object under another name
read it as an alias of a name that class never bound, and was left
without the attribute. Within one class body the object is bound once:
a second binding raises 'ReboundOverload'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject
from worktoy.waitaminute.meta import ReboundOverload

from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


def _intLoad(self: Any, n: int) -> tuple:
  return 'int', n


def _fallbackLoad(self: Any, *args) -> tuple:
  return 'fallback', args


class TestOverloadRebound(OverloadTest):
  """
  TestOverloadRebound provides tests for an 'overload' object bound in the
  bodies of two classes.
  """

  def test_second_class_other_name(self) -> None:
    """A second class binding the overload under another name dispatches
    it under that name."""
    ov = overload(int)(_intLoad)

    class Foo(BaseObject):
      foo = ov

    class Bar(BaseObject):
      bar = ov

    self.assertEqual(Foo().foo(1), ('int', 1))
    self.assertEqual(Bar().bar(2), ('int', 2))

  def test_second_class_fallback(self) -> None:
    """A fallback bound in a second class under another name is that
    class's fallback."""
    fb = overload.fallback(_fallbackLoad)

    class Foo(BaseObject):
      foo = fb

    class Bar(BaseObject):
      bar = fb

    self.assertEqual(Foo().foo(1), ('fallback', (1,)))
    self.assertEqual(Bar().bar(2, 3), ('fallback', (2, 3)))

  def test_second_class_same_name(self) -> None:
    """A second class binding the overload under the same name dispatches
    it as well."""
    ov = overload(int)(_intLoad)

    class Foo(BaseObject):
      baz = ov

    class Bar(BaseObject):
      baz = ov

    self.assertEqual(Foo().baz(1), ('int', 1))
    self.assertEqual(Bar().baz(2), ('int', 2))

  def test_second_binding_other_name_refused(self) -> None:
    """This method tests that binding an overload a second time in one
    class body, under another name as in '__radd__ = __add__', does not
    pass. It raises 'ReboundOverload' naming both names."""
    with self.assertRaises(ReboundOverload) as context:
      class Real(BaseObject):
        @overload(float)
        def __add__(self, other: float) -> str:
          return 'float'

        __radd__ = __add__

    self.assertEqual(context.exception.className, 'Real')
    self.assertEqual(context.exception.firstName, '__add__')
    self.assertEqual(context.exception.newName, '__radd__')

  def test_second_binding_same_name_refused(self) -> None:
    """This method tests that binding an overload a second time in one
    class body under the same name does not pass. It raises
    'ReboundOverload'."""
    ov = overload(int)(_intLoad)
    with self.assertRaises(ReboundOverload):
      class Foo(BaseObject):
        foo = ov
        foo = ov

  def test_subclass_rebinding_refused(self) -> None:
    """This method tests that a subclass body binding its overload of an
    inherited name a second time, as '__radd__ = __add__' beside an
    inherited '@overload(float)', does not pass. It raises
    'ReboundOverload'."""

    class Real(BaseObject):
      @overload(float)
      def __add__(self, other: float) -> str:
        return 'Real'

    with self.assertRaises(ReboundOverload):
      class Complex(Real):
        @overload(complex)
        def __add__(self, other: complex) -> str:
          return 'Complex'

        __radd__ = __add__

  def test_second_name_with_own_method(self) -> None:
    """This method tests that a second name given a method of its own, the
    replacement for a second binding, does not dispatch differently from
    the first name. 'z + 1' and '1 + z' both reach 'Real.__add__'."""

    class Real(BaseObject):
      @overload(float)
      def __add__(self, other: float) -> str:
        return 'Real'

      def __radd__(self, other: object) -> str:
        return self.__add__(other)

    class Complex(Real):
      @overload(complex)
      def __add__(self, other: complex) -> str:
        return 'Complex'

    z = Complex()
    self.assertEqual(z + 1, 'Real')
    self.assertEqual(1 + z, 'Real')
    self.assertEqual(1j + z, 'Complex')
