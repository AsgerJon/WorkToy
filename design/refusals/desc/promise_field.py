"""
RefusedField holds the refusals that belong with
'design.promises.desc.promise_field'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import Field
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import AccessError, ReadOnlyError
from worktoy.waitaminute.desc import ProtectedError, NamelessCallback


class RefusedField(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A read without a getter raises 'AccessError', a write without
  a setter 'ReadOnlyError', a deletion without a deleter 'ProtectedError',
  all 'AttributeError's; a lambda raises 'NamelessCallback'. Source: the
  'Field' docstring and its example.
  """

  def test_missing_accessors_1(self) -> None:
    class Circle(BaseObject):
      area = Field()
      perimeter = Field()

      @area.GET
      def _getArea(self) -> float:
        return 3.0

    circle = Circle()
    with self.assertRaises(Exception) as refused:
      _ = circle.perimeter
    self.assertIsInstance(refused.exception, AccessError)

  def test_missing_accessors_2(self) -> None:
    class Circle(BaseObject):
      area = Field()
      perimeter = Field()

      @area.GET
      def _getArea(self) -> float:
        return 3.0

    circle = Circle()
    with self.assertRaises(Exception) as refused:
      circle.area = 1.0
    self.assertIsInstance(refused.exception, ReadOnlyError)

  def test_missing_accessors_3(self) -> None:
    class Circle(BaseObject):
      area = Field()
      perimeter = Field()

      @area.GET
      def _getArea(self) -> float:
        return 3.0

    circle = Circle()
    with self.assertRaises(Exception) as refused:
      del circle.area
    self.assertIsInstance(refused.exception, ProtectedError)

  def test_lambda_refused(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Circle(BaseObject):
        radius = Field()
        radius.GET(lambda self: 1.0)
    self.assertIsInstance(refused.exception, NamelessCallback)
