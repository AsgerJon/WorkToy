"""
PromiseARGS promises 'ARGS' from 'worktoy.core.sentinels'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core.sentinels import ARGS


class PromiseARGS(TestCase):
  """
  'ARGS' marks the variadic tail of an overload signature, and
  'ARGS[int]' a tail of integers. Unlike the other sentinels it is
  subscripted to an instance carrying its inner type as
  '__inner_type__'. Two instances of one inner type are equal and hash
  alike, also when one comes from a subclass of 'ARGS', and differ from
  instances of other inner types and from the type itself. Starring an
  instance gives the instance, and starring 'ARGS' gives 'ARGS[object]',
  so '*ARGS[int]' and '*ARGS' read naturally in a signature. Source: the
  'ARGS' docstring, and the 1.1.0 changelog entry "An instance of a
  subclass of ARGS hashes as the equal ARGS instance".
  """

  def test_inner_type(self) -> None:
    self.assertIs(ARGS[int].__inner_type__, int)

  def test_equality(self) -> None:
    self.assertEqual(ARGS[int], ARGS[int])
    self.assertEqual(hash(ARGS[int]), hash(ARGS[int]))
    self.assertNotEqual(ARGS[int], ARGS[str])
    self.assertNotEqual(ARGS[int], int)

  def test_subclass_instance(self) -> None:
    class TAILARGS(ARGS):
      pass

    self.assertEqual(TAILARGS[int], ARGS[int])
    self.assertIn(ARGS[int], {TAILARGS[int]})

  def test_starred(self) -> None:
    self.assertEqual([*ARGS[int]], [ARGS[int]])
    self.assertEqual([*ARGS], [ARGS[object]])
