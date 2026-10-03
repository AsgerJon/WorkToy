"""
TestPlainBaseReservedIgnored subclasses 'EZTest' from the
'tests.test_ezdata' package and pins that a plain base, one not built by
'EZMeta', may define the methods EZData reserves for itself, and that
EZData's generated methods take precedence over them. A mixin may then
declare such a method as a placeholder for the protocol it is written
against, and an EZData class mixing it in supplies the real one.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.ezdata import EZData, EZField, EZSpace

from . import EZTest

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


#  Stands in for a reserved method on a plain base, and never runs.
_placeholder = lambda *args, **kwargs: 'placeholder'


class TestPlainBaseReservedIgnored(EZTest):
  """
  TestPlainBaseReservedIgnored provides tests for reserved methods defined
  on a plain base of an 'EZData' class.
  """

  def test_every_reserved_method_ignored(self) -> None:
    """
    Testing that each reserved method a plain base defines is accepted and
    replaced on the EZData class by the generated one, in either base
    order.
    """
    for name in EZSpace.__reserved_ez_methods__:
      with self.subTest(name=name):
        mixin = type('Mixin', (), {name: _placeholder})

        class First(EZData, mixin):
          x = EZField[int](0)

        class Last(mixin, EZData):
          x = EZField[int](0)

        self.assertIsNot(getattr(First, name), _placeholder)
        self.assertIsNot(getattr(Last, name), _placeholder)

  def test_protocol_mixin(self) -> None:
    """
    Testing that a mixin written against construction and iteration works
    through the generated methods, its own placeholders ignored.
    """

    class Geometry:
      def __init__(self, *args: float) -> None:
        pass

      def __iter__(self) -> Any:
        yield from ()

      def __len__(self) -> int:
        return 0

      def magnitude(self) -> float:
        return sum(x ** 2 for x in self) ** 0.5

      def __neg__(self) -> Any:
        return type(self)(*(-x for x in self))

    class Point(EZData, Geometry):
      x = EZField[float](0.0)
      y = EZField[float](0.0)

    point = Point(3.0, 4.0)
    self.assertEqual(point.magnitude(), 5.0)
    self.assertEqual(-point, Point(-3.0, -4.0))
    self.assertEqual(len(point), 2)
    self.assertEqual(list(Geometry()), [])
