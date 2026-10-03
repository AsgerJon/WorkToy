"""
TestKeeNumberDefault subclasses 'KeeTest' and pins that the value of a
'Kee' member of a number type is built by the rules of 'AttriBox', which
'Kee' is based on: a value the lossless cast refuses is refused at the
class statement, where 'Kee[int](2.5)' used to give the member the value
'2'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from worktoy.keenum import KeeNum, Kee
from worktoy.waitaminute import TypeException

from . import KeeTest


class TestKeeNumberDefault(KeeTest):
  """
  TestKeeNumberDefault provides tests for the number values of 'Kee'
  members.
  """

  def test_lossy_value_refused(self) -> None:
    """A member value the lossless cast refuses raises 'TypeException' at
    the class statement."""
    with self.assertRaises(TypeException):
      class Bad(KeeNum):
        A = Kee[int](1)
        B = Kee[int](2.5)

  def test_cast_value_kept(self) -> None:
    """A member value the cast converts without loss is the value of the
    member, as an instance of the declared type."""

    class Real(KeeNum):
      A = Kee[float](1)

    class Whole(KeeNum):
      B = Kee[int]('7')

    self.assertIs(type(Real.A.value), float)
    self.assertEqual(Real.A.value, 1.0)
    self.assertEqual(Whole.B.value, 7)
