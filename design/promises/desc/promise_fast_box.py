"""
PromiseFastBox promises 'FastBox' from 'worktoy.desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import FastBox
from worktoy.mcls import BaseObject


class PromiseFastBox(TestCase):
  """
  'FastBox' is the strict, fast box. 'mass = FastBox[float](1)' takes one
  value, converted once on the declaration line, which every instance shares
  until it assigns its own; empty parentheses give each instance a new
  'fieldType()' instead. A shared value must be hashable. An assigned value
  must be an instance of the field type already, a 'bool' passing for an
  'int', with no conversion. After a deletion the next read starts over from
  the declared value. Source: the 'FastBox' docstring.
  """

  def test_shared_value(self) -> None:
    class Particle(BaseObject):
      mass = FastBox[float](1)

    particle = Particle()
    self.assertEqual(particle.mass, 1.0)
    self.assertIs(type(particle.mass), float)
    particle.mass = 5.0
    self.assertEqual(particle.mass, 5.0)
    self.assertEqual(Particle().mass, 1.0)
    del particle.mass
    self.assertEqual(particle.mass, 1.0)

  def test_new_value_per_instance(self) -> None:
    class Particle(BaseObject):
      tags = FastBox[list]()

    self.assertEqual(Particle().tags, [])
    self.assertIsNot(Particle().tags, Particle().tags)

  def test_instance_check(self) -> None:
    class Counter(BaseObject):
      count = FastBox[int](0)

    counter = Counter()
    counter.count = True
    self.assertIs(counter.count, True)
