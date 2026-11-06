"""
TestSamplerMeta tests 'SamplerMeta' from 'worktoy.work_test.samplers'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from abc import ABCMeta

from worktoy.desc import AttriBox
from worktoy.mcls import BaseMeta
from worktoy.work_test.samplers import SamplerMeta, BaseSampler, IntSampler
from . import WorkTestTest, Half


class TestSamplerMeta(WorkTestTest):
  """
  'SamplerMeta' is 'BaseMeta' combined with 'ABCMeta', so a sampler body
  keeps the hooks and overloads of a worktoy class while a class leaving
  a hook abstract is refused when built. The tests pin the bases, the
  metaclass of the samplers, the refusal of 'Half' and the acceptance of
  the die sampler of the 'BaseSampler' docstring.
  """

  def test_bases(self) -> None:
    self.assertEqual(SamplerMeta.__bases__[:2], (BaseMeta, ABCMeta))
    self.assertIsSubclass(SamplerMeta, ABCMeta)
    self.assertLess(SamplerMeta.__mro__.index(BaseMeta),
                    SamplerMeta.__mro__.index(ABCMeta))
    self.assertIs(type(BaseSampler), SamplerMeta)
    self.assertIs(type(IntSampler), SamplerMeta)
    self.assertIs(type(Half), SamplerMeta)
    self.assertEqual(BaseSampler.__abstractmethods__,
                     frozenset(('_getValueType', '_getItem')))

  def test_half_refused(self) -> None:
    self.assertIs(Half._getValueType(None), int)
    self.assertEqual(Half.__abstractmethods__, frozenset(('_getItem',)))
    with self.assertRaises(TypeError):
      Half()

  def test_docstring_die_accepted(self) -> None:
    class DieSampler(BaseSampler):
      sides = AttriBox[int](6)

      def _getValueType(self, **kwargs) -> type:
        return int

      def _getItem(self, *args, **kwargs) -> int:
        return self.random.randint(1, self.sides)

    self.assertEqual(DieSampler.__abstractmethods__, frozenset())
    die = DieSampler(seed=5, size=4)
    self.assertIs(die.valueType, int)
    row = die.row
    self.assertEqual(len(row), 4)
    for value in row:
      with self.subTest(value=value):
        self.assertIn(value, range(1, 7))
    self.assertEqual(DieSampler(seed=5, size=4).row, row)
