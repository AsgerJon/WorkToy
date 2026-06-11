"""
TestKeeMetaSubClass subclasses 'KeeTest' and tests subclassing of
'KeeMeta'. Because 'KeeMeta' creates 'KeeNum' in an unconventional way,
this verifies that a 'KeeMeta' subclass (here 'KeeMetaSub') provides its
own distinct 'KeeNum'-like class via the 'keeNum' descriptor.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from tests.test_keenum import KeeTest
from worktoy.keenum import KeeMeta, KeeNum, Kee, KeeMetaMeta
from worktoy.mcls import BaseMeta


class KeeMetaSub(KeeMeta):
  """
  KeeMetaSub is a 'KeeMeta' subclass used as a fixture. Because
  'KeeMeta' creates 'KeeNum' in an unconventional way, deriving from
  'KeeMeta' must give this subclass its own distinct 'KeeNum'-like
  class via the 'keeNum' descriptor.
  """


class SubNum(KeeMetaSub.keeNum):
  """
  This class demonstrates the syntax required for creating an enumerating
  class using as metaclass a subclass of 'KeeMeta' rather than 'KeeMeta'
  itself. The 'KeeNum' class is identical to the 'KeeMeta.keeNum' value.
  To derive an enumerating class from a subclass of 'KeeMeta', set as base
  class the 'keeNum' attribute of the custom metaclass.
  """

  TOM = Kee[int](69)
  DICK = Kee[int](420)
  HARRY = Kee[int](1337)


class TestKeeMetaSubClass(KeeTest):
  """
  TestKeeMetaSubClass subclasses 'KeeTest' and tests subclassing of
  'KeeMeta'. Because 'KeeMeta' creates 'KeeNum' in an unconventional
  way, this verifies that a 'KeeMeta' subclass (here 'KeeMetaSub')
  provides its own distinct 'KeeNum'-like class via 'keeNum'.
  """

  def test_kee_meta(self, ) -> None:
    """
    This method tests the 'keeNum' descriptor on the 'KeeMeta' class.
    """
    self.assertIsInstance(KeeMeta.keeNum, KeeMeta)
    self.assertIs(KeeMeta.keeNum, KeeNum)

  def test_kee_meta_sub_class(self) -> None:
    """
    Tests that 'KeeMetaSub' subclasses 'KeeMeta' and provides its own
    'KeeNum'-like class.
    """
    KeeMetaSubNum = KeeMetaSub.keeNum
    self.assertIsInstance(KeeMetaSubNum, KeeMetaSub)
    self.assertIsNot(KeeMetaSubNum, KeeNum)
    self.assertIs(KeeMetaSub.keeNum, KeeMetaSubNum)

  def test_sub_num(self) -> None:
    """
    Tests that 'SubNum' is an enumerating class using 'KeeMetaSub' as
    metaclass.
    """
    self.assertIsInstance(SubNum, KeeMetaSub)
    self.assertIsSubclass(SubNum, KeeMetaSub.keeNum)
    for member in SubNum:
      self.assertIsInstance(member, SubNum)

  def test_kee_num_recursion(self) -> None:
    """
    Tests the recursion guard in the 'KeeMetaMeta.keeNum' descriptor.
    """

    class Num(BaseMeta, metaclass=KeeMetaMeta):
      pass

    with self.assertRaises(RecursionError):
      _ = Num._getKeeNum(_recursion=True)
