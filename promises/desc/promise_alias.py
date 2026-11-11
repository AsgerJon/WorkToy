"""
PromiseAlias promises 'Alias' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox, Alias
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import DanglingAlias, NotADescriptor
from worktoy.waitaminute.desc import ReadOnlyError


class PromiseAlias(TestCase):
  """
  'w = Alias('width')' gives the attribute 'width' a second name: both
  read, write and delete the very same value, the name may be held by a
  base, and the alias follows a subclass that redeclares 'width'. A
  method may be aliased too, and a
  write through such an alias raises 'ReadOnlyError'. Read through the
  class, the alias is itself. As the class is created, a name no class
  holds raises 'DanglingAlias' and a name holding a plain value raises
  'NotADescriptor'. Source: the 'Alias' docstring and its example.
  """

  def test_second_name(self) -> None:
    class Geometry(BaseObject):
      width = AttriBox[int](240)
      w = Alias('width')

    geometry = Geometry()
    geometry.w = 300
    self.assertEqual(geometry.width, 300)
    self.assertEqual(geometry.w, 300)
    self.assertIsInstance(Geometry.w, Alias)

  def test_follows_redeclaration(self) -> None:
    class Geometry(BaseObject):
      width = AttriBox[int](240)
      w = Alias('width')

    class Wide(Geometry):
      width = AttriBox[int](999)

    self.assertEqual(Wide().w, 999)

  def test_same_callbacks(self) -> None:
    log = []

    class Geometry(BaseObject):
      width = AttriBox[int](240)
      w = Alias('width')

      @width.onSet
      def _resized(self, value: int) -> None:
        log.append(value)

    Geometry().w = 300
    self.assertEqual(log, [300])

  def test_target_in_base(self) -> None:
    class Geometry(BaseObject):
      width = AttriBox[int](240)

    class Short(Geometry):
      w = Alias('width')

    self.assertEqual(Short().w, 240)

  def test_method(self) -> None:
    class Geometry(BaseObject):
      width = AttriBox[int](240)

      def doubled(self) -> int:
        return 2 * self.width

      twice = Alias('doubled')

    geometry = Geometry()
    self.assertEqual(geometry.twice(), 480)
    with self.assertRaises(ReadOnlyError):
      geometry.twice = None

  def test_refusals(self) -> None:
    with self.assertRaises((DanglingAlias, RuntimeError)) as context:
      class Dangling(BaseObject):
        w = Alias('nothing')
    refusal = context.exception.__cause__ or context.exception
    self.assertIsInstance(refusal, DanglingAlias)
    self.assertEqual(refusal.realName, 'nothing')
    with self.assertRaises((NotADescriptor, RuntimeError)) as context:
      class Plain(BaseObject):
        x = 3
        w = Alias('x')
    refusal = context.exception.__cause__ or context.exception
    self.assertIsInstance(refusal, NotADescriptor)
    self.assertEqual(refusal.realName, 'x')
    self.assertEqual(refusal.found, 3)
