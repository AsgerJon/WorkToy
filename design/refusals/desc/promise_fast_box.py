"""
RefusedFastBox holds the refusals that belong with
'design.promises.desc.promise_fast_box'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import FastBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute import TypeException
from worktoy.waitaminute.dispatch import TypeCastException


class RefusedFastBox(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A value that is no instance of the field type, as '2' for a
  'FastBox[float]', raises 'TypeException'. A box declared without
  parentheses, given an unhashable value, or called again on the class raises
  'TypeError'. Source: the 'FastBox' docstring.
  """

  def test_no_conversion_on_write(self) -> None:
    class Particle(BaseObject):
      mass = FastBox[float](1.0)

    particle = Particle()
    with self.assertRaises(Exception) as refused:
      particle.mass = 2
    self.assertIsInstance(refused.exception, TypeException)

  def test_declaration_refusals_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      class NoParentheses(BaseObject):
        mass = FastBox[float]
    self.assertIsInstance(refused.exception, (TypeError, RuntimeError))

  def test_declaration_refusals_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Unhashable(BaseObject):
        tags = FastBox[list](['a'])
    self.assertIsInstance(refused.exception, (TypeError, RuntimeError))

  def test_declaration_refusals_3(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Wrong(BaseObject):
        count = FastBox[int]('a')
    self.assertIsInstance(refused.exception, TypeCastException)

  def test_declaration_refusals_4(self) -> None:
    class Particle(BaseObject):
      mass = FastBox[float](1.0)

    with self.assertRaises(Exception) as refused:
      Particle.mass(9.0)
    self.assertIsInstance(refused.exception, TypeError)
