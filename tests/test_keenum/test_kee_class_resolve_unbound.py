"""
TestKeeClassResolveUnbound subclasses 'KeeTest' and pins that the class
body of a 'KeeNum' refuses a '__class_resolve__' that is not a
classmethod, with 'UnboundClassHook' at the line binding it, as the
namespace refuses one of the routed '__class_*__' hooks. Only callability
used to be checked, so a plain function passed, and every lookup reaching
the hook called it without the class and raised Python's own
'TypeError'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute.meta import UnboundClassHook

from . import KeeTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


class TestKeeClassResolveUnbound(KeeTest):
  """
  TestKeeClassResolveUnbound provides tests for a '__class_resolve__'
  defined without '@classmethod'.
  """

  def test_plain_function_refused(self) -> None:
    """A plain function is refused, naming the class and the hook."""
    with self.assertRaises(UnboundClassHook) as context:
      class Num(KeeNum):
        A = Kee[int](1)

        def __class_resolve__(cls, identifier: Any) -> Any:
          return NotImplemented  # pragma: no cover
    self.assertEqual(context.exception.className, 'Num')
    self.assertEqual(context.exception.hookName, '__class_resolve__')

  def test_staticmethod_refused(self) -> None:
    """A staticmethod is refused."""
    with self.assertRaises(UnboundClassHook):
      class Num(KeeNum):
        A = Kee[int](1)

        @staticmethod
        def __class_resolve__(identifier: Any) -> Any:
          return NotImplemented  # pragma: no cover

  def test_classmethod_accepted(self) -> None:
    """A classmethod is accepted and consulted."""

    class Num(KeeNum):
      A = Kee[int](1)

      @classmethod
      def __class_resolve__(cls, identifier: Any) -> Any:
        return cls.A if identifier == 'first' else NotImplemented

    self.assertIs(Num('first'), Num.A)
    self.assertIs(Num(1), Num.A)
