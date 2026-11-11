"""
PromiseField promises 'Field' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import Field
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import AccessError, ReadOnlyError
from worktoy.waitaminute.desc import ProtectedError, NamelessCallback


class PromiseField(TestCase):
  """
  A 'Field' is an attribute computed or guarded by methods of the class,
  as a 'property' is: 'GET' registers the getter, a second one replacing
  the first, and 'SET' and 'DELETE' any number of setters and deleters,
  run in the order registered. Unlike a
  'property', the methods are found by name at each access, so a
  subclass overriding one changes the attribute without declaring it
  again. A read without a getter raises 'AccessError', a write without a
  setter 'ReadOnlyError', a deletion without a deleter 'ProtectedError',
  all 'AttributeError's; a lambda raises 'NamelessCallback'. Source: the
  'Field' docstring and its example.
  """

  def test_get_and_set(self) -> None:
    log = []

    class Circle(BaseObject):
      __radius__ = 1.0
      radius = Field()

      @radius.GET
      def _getRadius(self) -> float:
        return self.__radius__

      @radius.SET
      def _setRadius(self, value: float) -> None:
        self.__radius__ = value

      @radius.SET
      def _logRadius(self, value: float) -> None:
        log.append(value)

    circle = Circle()
    self.assertEqual(circle.radius, 1.0)
    circle.radius = 2.0
    self.assertEqual(circle.radius, 2.0)
    self.assertEqual(log, [2.0])

  def test_second_getter_replaces(self) -> None:
    class Circle(BaseObject):
      radius = Field()

      @radius.GET
      def _getOld(self) -> float:
        return 1.0

      @radius.GET
      def _getNew(self) -> float:
        return 2.0

    self.assertEqual(Circle().radius, 2.0)

  def test_override_without_redeclaring(self) -> None:
    class Circle(BaseObject):
      __radius__ = 1.0
      radius = Field()

      @radius.GET
      def _getRadius(self) -> float:
        return self.__radius__

    class BigCircle(Circle):
      def _getRadius(self) -> float:
        return 10 * self.__radius__

    self.assertEqual(BigCircle().radius, 10.0)

  def test_missing_accessors(self) -> None:
    class Circle(BaseObject):
      area = Field()
      perimeter = Field()

      @area.GET
      def _getArea(self) -> float:
        return 3.0

    circle = Circle()
    with self.assertRaises(AccessError) as context:
      _ = circle.perimeter
    self.assertIs(context.exception.desc, vars(Circle)['perimeter'])
    with self.assertRaises(ReadOnlyError) as context:
      circle.area = 1.0
    self.assertIs(context.exception.instance, circle)
    self.assertIs(context.exception.desc, vars(Circle)['area'])
    self.assertEqual(context.exception.newVal, 1.0)
    with self.assertRaises(ProtectedError) as context:
      del circle.area
    self.assertIs(context.exception.instance, circle)
    self.assertIs(context.exception.desc, vars(Circle)['area'])
    #  'oldVal' holds the value only "if known".
    self.assertIn(context.exception.oldVal, (None, 3.0))
    for error in (AccessError, ReadOnlyError, ProtectedError):
      with self.subTest(error=error.__name__):
        self.assertTrue(issubclass(error, AttributeError))

  def test_lambda_refused(self) -> None:
    with self.assertRaises(NamelessCallback) as context:
      class Circle(BaseObject):
        radius = Field()
        radius.GET(lambda self: 1.0)
    self.assertEqual(context.exception.role, 'GET')
