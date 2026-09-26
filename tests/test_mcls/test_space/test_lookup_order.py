"""
TestLookupOrder subclasses 'MCLSTest' and pins where 'BaseSpace' looks for
inherited overload registrations when its bases admit no consistent
method resolution order. Passing '_strictMRO=False' accepts such bases
anyway, leaving the namespace without a resolved order. The namespace
then walks each base's own order instead, bases left to right, skipping
classes it has already visited.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.dispatch import overload, TypeSig
from worktoy.mcls import BaseObject, BaseMeta, BaseSpace
from .. import MCLSTest


class First(BaseObject):
  """First registers 'describe' for an 'int'."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def describe(self, n: int) -> str:
    return 'first'  # pragma: no cover


class Second(BaseObject):
  """Second registers 'describe' for an 'int', colliding with 'First',
  and for a 'str', which 'First' lacks."""

  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  #  DOMAIN SPECIFIC  # # # # # # # # # # # # # # # # # # # # # # # # # # # #
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

  @overload(int)
  def describe(self, n: int) -> str:
    return 'second'  # pragma: no cover

  @overload(str)
  def describe(self, s: str) -> str:
    return 'second'  # pragma: no cover


class FirstThenSecond(First, Second):
  """FirstThenSecond demands 'First' before 'Second'."""


class SecondThenFirst(Second, First):
  """SecondThenFirst demands 'Second' before 'First', contradicting
  'FirstThenSecond'."""


class TestLookupOrder(MCLSTest):
  """
  TestLookupOrder pins the lookup order a 'BaseSpace' falls back to when
  its bases admit no consistent method resolution order.
  """

  def setUp(self) -> None:
    """
    The namespace is built directly, since no class can be created from
    bases that contradict each other.
    """
    super().setUp()
    bases = (FirstThenSecond, SecondThenFirst)
    self.space = BaseSpace(BaseMeta, 'Neither', bases, _strictMRO=False)

  def test_no_resolved_order(self) -> None:
    """
    Testing that the namespace holds no resolved method resolution
    order, which is what makes it fall back.
    """
    self.assertIsNone(self.space.getMRO())

  def test_first_base_order_wins(self) -> None:
    """
    Testing that the registrations follow the order of the first base,
    'FirstThenSecond': 'First' wins the colliding 'int' signature, while
    the 'str' signature only 'Second' registers is still found.
    """
    collected = self.space.collectOverloads('describe')
    sigs = [sig for sig, _, __ in collected]
    self.assertEqual(sigs, [TypeSig(int), TypeSig(str)])
    firstFunc = First.__namespace__.getOverloads()['describe'][0][1]
    self.assertIs(collected[0][1], firstFunc)
