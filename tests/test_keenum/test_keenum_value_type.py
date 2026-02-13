"""
TestKeeNumValueType tests the added 'valueType' descriptor exposing the
type of the values of the enumeration members. This is a useful addition
to the 'KeeNum' class, as it allows for more robust type checking and error
handling when working with enumeration members and their values.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from worktoy.keenum import Kee, KeeNum
from worktoy.waitaminute import TypeException
from . import KeeTest, examples

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestKeeNumValueType(KeeTest):
  """
  TestKeeNumValueType tests the added 'valueType' descriptor exposing the
  type of the values of the enumeration members. This is a useful addition
  to the 'KeeNum' class, as it allows for more robust type checking and error
  handling when working with enumeration members and their values.
  """

  @classmethod
  def setUpClass(cls, ) -> None:
    """Sets up the test class by creating the example enumeration."""
    super().setUpClass()
    cls.exampleClasses = (
      examples.RGBNum,
      examples.WeekDay,
      examples.Compass,
      examples.Month,
    )
    cls.exampleValueTypes = (
      examples.RGB,
      str,
      complex,
      str,
    )

  def test_examples(self, ) -> None:
    """Tests the examples provided in the documentation."""
    for cls, type_ in zip(self.exampleClasses, self.exampleValueTypes, ):
      self.assertIs(cls.valueType, type_)

  def test_bad_value_type(self, ) -> None:
    """
    Testing the error handling when an enumeration has inconsistent value
    types among its members.
    """

    with self.assertRaises(TypeException) as context:
      class Breh(KeeNum):
        A = Kee[str]('lol')
        B = Kee[str]('69')

      setattr(Breh.B.kee, '__field_value__', 69)
      _ = Breh.valueType
    e = context.exception
    self.assertEqual(e.varName, '__field_value__')
    self.assertEqual(e.actualObject, 69)
    self.assertIs(e.actualType, int)
    self.assertIn(str, e.expectedTypes)
