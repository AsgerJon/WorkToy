"""
TestOverloadReplacesPlain subclasses 'OverloadTest' and pins that a
subclass overloading a name its parent defines as a plain method
replaces that method with the 'Dispatcher' its overloads build. The plain
method of the parent takes no part in the dispatch: a call matching none
of the subclass's signatures raises 'DispatchException' rather than
reaching it.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.dispatch import overload, Dispatcher
from worktoy.mcls import BaseObject
from worktoy.waitaminute.dispatch import DispatchException

from . import OverloadTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestOverloadReplacesPlain(OverloadTest):
  """
  TestOverloadReplacesPlain provides tests for subclasses overloading a
  name their parent defines plainly.
  """

  def test_dispatcher_replaces_plain(self) -> None:
    """The subclass holds a 'Dispatcher' over its own signatures alone,
    and the parent keeps its plain method."""

    class Parent(BaseObject):
      def bar(self, *args: Any) -> str:
        return 'parent plain'

    class Child(Parent):
      @overload(int)
      def bar(self, x: int) -> str:
        return 'child int'

    self.assertIsInstance(Child.__dict__['bar'], Dispatcher)
    self.assertEqual(Child().bar(1), 'child int')
    with self.assertRaises(DispatchException):
      Child().bar(object())
    self.assertEqual(Parent().bar(object()), 'parent plain')
