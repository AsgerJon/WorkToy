"""
RefusedAlias holds the refusals that belong with
'design.promises.desc.promise_alias'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox, Alias
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import DanglingAlias, NotADescriptor
from worktoy.waitaminute.desc import ReadOnlyError


class RefusedAlias(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A write through the alias of a method raises 'ReadOnlyError'.
  As the class is created, a name no class holds raises 'DanglingAlias' and a
  name holding a plain value raises 'NotADescriptor'. Source: the 'Alias'
  docstring and its example.
  """

  def test_method(self) -> None:
    class Geometry(BaseObject):
      width = AttriBox[int](240)

      def doubled(self) -> int:
        return 2 * self.width

      twice = Alias('doubled')

    geometry = Geometry()
    with self.assertRaises(Exception) as refused:
      geometry.twice = None
    self.assertIsInstance(refused.exception, ReadOnlyError)

  def test_refusals_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Dangling(BaseObject):
        w = Alias('nothing')
    self.assertIsInstance(refused.exception, (DanglingAlias, RuntimeError))

  def test_refusals_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Plain(BaseObject):
        x = 3
        w = Alias('x')
    self.assertIsInstance(refused.exception, (NotADescriptor, RuntimeError))
