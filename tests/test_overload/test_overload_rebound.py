"""
TestOverloadRebound subclasses 'OverloadTest' and pins that one 'overload'
object bound in the bodies of two classes builds a 'Dispatcher' in each,
whatever name each binds it to. The name a class body claimed an overload
under used to be written on the overload object itself, where it outlived
the class body, so a second class binding the object under another name
read it as an alias of a name that class never bound, and was left
without the attribute.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload
from worktoy.mcls import BaseObject

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

  def test_alias_within_second_class(self) -> None:
    """Within the second class, a further binding of the overload under a
    third name is an alias of the name that class bound it to first."""
    ov = overload(int)(_intLoad)

    class Foo(BaseObject):
      foo = ov

    class Bar(BaseObject):
      bar = ov

      @overload(str)
      def bar(self, s: str) -> tuple:
        return 'str', s

      baz = bar

    self.assertEqual(Bar().baz(3), ('int', 3))
    self.assertEqual(Bar().baz('x'), ('str', 'x'))
