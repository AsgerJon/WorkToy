"""
TestFullName subclasses 'EZExamplesTest' from the
'tests.test_ezdata.examples._ez_examples_test' package and provides tests for
the 'FullName' class from the 'tests.test_ezdata.examples' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from tests.test_ezdata.examples import FullName
from . import EZExamplesTest

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestFullName(EZExamplesTest):
  """
  TestFullName subclasses 'EZExamplesTest' from the
  'tests.test_ezdata.examples._ez_examples_test' package and provides tests
  for the 'FullName' class from the 'tests.test_ezdata.examples' package.
  """

  def setUp(self) -> None:
    super().setUp()
    self.agf2026: tuple[FullName, ...] = (
      # Keepers
      FullName('Hansen', 'Jesper'),
      FullName('Christiansen', 'Mads Hedenstad'),
      # Defence
      FullName('Dalsgaard', 'Henrik'),
      FullName('Beijmo', 'Felix'),
      FullName('Kahl', 'Eric'),
      FullName('Tingager', 'Frederik'),
      FullName('Mølgaard', 'Tobias'),
      FullName('Andersen', 'Jacob Florentin'),
      FullName('Jensen-Abbew', 'Jonas'),
      FullName('Carstensen', 'Rasmus'),
      # Midfield
      FullName('Solbakken', 'Markus'),
      FullName('Knudsen', 'Magnus'),
      FullName('Poulsen', 'Nicolai'),
      FullName('Links', 'Gift'),
      FullName('Yakob', 'Kevin'),
      FullName('Arnstad', 'Kristian'),
      # Forwards
      FullName('Mortensen', 'Patrick'),  # captain
      FullName('Kristensen', 'Tobias Bech'),
      FullName('Jørgensen', 'Sebastian'),
      FullName('Serra', 'Janni'),
      FullName('Gyamfi', 'Richmond'),
      FullName('Emmery', 'Frederik'),
      FullName('Tchamche', 'Stefen'),
      FullName('Bogere', 'James'),
    )

  def test_init(self, ) -> None:
    """
    This method tests initialization of 'FullName' with different number of
    arguments.
    """
    name = FullName()
    self.assertFalse(name.givenNames)
    self.assertFalse(name.familyName)

    name = FullName('Rick')
    self.assertEqual(name.givenNames, 'Rick')
    self.assertFalse(name.familyName)

    name = FullName('Rick', 'Astley')
    self.assertEqual(name.givenNames, 'Rick')
    self.assertEqual(name.familyName, 'Astley')

  def test_order(self, ) -> None:
    """
    This method tests the ordering of 'FullName' instances.
    """
    names = sorted(self.agf2026)
    expectedFirst = FullName('Andersen', 'Jacob Florentin')
    expectedLast = FullName('Yakob', 'Kevin')
    self.assertEqual(names[0], expectedFirst)
    self.assertEqual(names[-1], expectedLast)

  def test_lt(self, ) -> None:
    """
    This method tests the '__lt__' operator on 'FullName' instances.
    The operator compares the tuple of field values in declaration
    order and returns True only when 'self' is strictly less than
    'other'. Equal instances return False, and comparison against an
    unrelated type returns 'NotImplemented' so Python can fall back
    to the reflected operator.
    """
    early = FullName('Andersen', 'Jacob Florentin')
    late = FullName('Yakob', 'Kevin')
    same = FullName('Andersen', 'Jacob Florentin')

    self.assertTrue(early < late)
    self.assertFalse(late < early)
    self.assertFalse(early < same)
    self.assertIs(FullName.__lt__(early, 'Andersen'), NotImplemented)

  def test_le(self, ) -> None:
    """
    This method tests the '__le__' operator on 'FullName' instances.
    The operator returns True when 'self' is less than or equal to
    'other', so equal instances return True. Comparison against an
    unrelated type returns 'NotImplemented'.
    """
    early = FullName('Andersen', 'Jacob Florentin')
    late = FullName('Yakob', 'Kevin')
    same = FullName('Andersen', 'Jacob Florentin')

    self.assertTrue(early <= late)
    self.assertTrue(early <= same)
    self.assertFalse(late <= early)
    self.assertIs(FullName.__le__(early, 'Andersen'), NotImplemented)

  def test_gt(self, ) -> None:
    """
    This method tests the '__gt__' operator on 'FullName' instances.
    The operator compares the tuple of field values in declaration
    order and returns True only when 'self' is strictly greater than
    'other'. Equal instances return False, and comparison against an
    unrelated type returns 'NotImplemented'.
    """
    early = FullName('Andersen', 'Jacob Florentin')
    late = FullName('Yakob', 'Kevin')
    same = FullName('Yakob', 'Kevin')

    self.assertTrue(late > early)
    self.assertFalse(early > late)
    self.assertFalse(late > same)
    self.assertIs(FullName.__gt__(late, 'Yakob'), NotImplemented)

  def test_ge(self, ) -> None:
    """
    This method tests the '__ge__' operator on 'FullName' instances.
    The operator returns True when 'self' is greater than or equal
    to 'other', so equal instances return True. Comparison against
    an unrelated type returns 'NotImplemented'.
    """
    early = FullName('Andersen', 'Jacob Florentin')
    late = FullName('Yakob', 'Kevin')
    same = FullName('Yakob', 'Kevin')

    self.assertTrue(late >= early)
    self.assertTrue(late >= same)
    self.assertFalse(early >= late)
    self.assertIs(FullName.__ge__(late, 'Yakob'), NotImplemented)

  def test_alphabetical_order(self, ) -> None:
    """
    This method tests that 'FullName' instances sort into a strict
    alphabetical sequence by '(givenNames, familyName)'. The order
    produced by 'sorted' on the squad tuple is compared to the order
    produced by Python's native string-tuple sort on the same pairs;
    the two must match for every position, not just at the endpoints.
    """
    ezSorted = sorted(self.agf2026)
    pairs = [(fn.givenNames, fn.familyName) for fn in self.agf2026]
    expected = sorted(pairs)
    actual = [(fn.givenNames, fn.familyName) for fn in ezSorted]
    self.assertEqual(actual, expected)

  def test_str(self, ) -> None:
    """
    This method tests the string representation of 'FullName' instances.
    The string is formatted as '<FullName: field1=value1, field2=value2>'.
    """
    for mester in self.agf2026:
      strMester = str(mester)
      self.assertIn(mester.familyName, strMester)
      for firstName in mester.givenNames.split():
        self.assertIn(firstName, strMester)
