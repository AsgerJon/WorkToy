"""
TestArgs tests 'ARGS' from 'worktoy.core.sentinels'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.core.sentinels import ARGS, SentinelMeta
from worktoy.core.sentinels._args import _MetaARGS
from . import CoreTest


class TestArgs(CoreTest):
  """
  'ARGS[int]' marks the variadic tail of an overload signature, and
  unlike every other sentinel it is instantiable, carrying the inner
  type. Two instances of one inner type must compare and hash alike,
  the class iterates to 'ARGS[object]' so '*ARGS' reads naturally, and
  an instance iterates to itself. The tests pin each of these, the
  text, and that 'ARGS' is still a registered sentinel.
  """

  def test_subscript_and_call_build_instances(self) -> None:
    tail = ARGS[int]
    self.assertIsInstance(tail, ARGS)
    self.assertIs(tail.__inner_type__, int)
    self.assertIs(ARGS(str).__inner_type__, str)
    self.assertIsNone(ARGS.__inner_type__)
    self.assertIsNot(ARGS[int], ARGS[int])

  def test_equality_by_inner_type(self) -> None:
    self.assertEqual(ARGS[int], ARGS[int])
    self.assertNotEqual(ARGS[int], ARGS[bool])
    self.assertIs(ARGS[int].__eq__(5), NotImplemented)
    self.assertFalse(ARGS[int] == 5)
    self.assertFalse(ARGS[int] == ARGS)
    self.assertTrue(ARGS[int] != ARGS[float])

  def test_hash(self) -> None:
    self.assertEqual(hash(ARGS[int]), hash(('ARGS', int)))
    self.assertEqual(hash(ARGS[int]), hash(ARGS[int]))
    self.assertNotEqual(hash(ARGS[int]), hash(int))
    self.assertEqual(len({ARGS[int], ARGS[int], ARGS[str]}), 2)

  def test_iteration(self) -> None:
    self.assertEqual([*ARGS], [ARGS[object]])
    self.assertEqual((*ARGS[int],), (ARGS[int],))
    self.assertEqual([*ARGS[str]][0].__inner_type__, str)

  def test_text(self) -> None:
    self.assertEqual(str(ARGS[int]), 'ARGS[int]')
    self.assertEqual(repr(ARGS[int]), 'ARGS[int]')
    self.assertEqual(str(ARGS[None]), 'ARGS[None]')
    self.assertEqual(str(ARGS), "<Sentinel: 'ARGS'>")

  def test_registered_sentinel(self) -> None:
    self.assertIn(ARGS, SentinelMeta._getRegisteredSentinels())
    self.assertIs(type(ARGS), _MetaARGS)
    self.assertIsInstance(ARGS, SentinelMeta)

  def test_subclass_instances_equal_by_inner_type(self) -> None:
    class CORE_TAIL(ARGS):
      pass

    self.assertEqual(CORE_TAIL[int], ARGS[int])
    self.assertEqual(ARGS[int], CORE_TAIL[int])
    self.assertEqual(hash(CORE_TAIL[int]), hash(ARGS[int]))
    self.assertEqual(str(CORE_TAIL[int]), 'CORE_TAIL[int]')
    self.assertIn(CORE_TAIL, SentinelMeta._getRegisteredSentinels())
