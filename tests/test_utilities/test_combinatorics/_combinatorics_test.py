"""
CombinatoricsTest subclasses 'UtilitiesTest' from the
'tests.test_utilities' package. It provides the test base for tests of the
'worktoy.utilities.combinatorics' package.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen

from .. import UtilitiesTest


class CombinatoricsTest(UtilitiesTest):
  """
  CombinatoricsTest subclasses 'UtilitiesTest' from the
  'tests.test_utilities' package. It provides the test base for tests of the
  'worktoy.utilities.combinatorics' package.
  """

  @classmethod
  def factorial(cls, n: int) -> int:
    """
    Compute the factorial of a number.

    Args:
        n (int): The number to compute the factorial of.

    Returns:
        int: The factorial of the number.
    """
    if n < 0:
      raise ValueError("""Domain error: n must be a non-negative integer.""")
    if n in (0, 1):
      return 1
    return n * cls.factorial(n - 1)

  def test_good_faculty(self, ) -> None:
    """
    This method provides tests for the 'factorial' method of the
    'CombinatoricsTest' class.
    """

    for i in range(2, 8):
      self.assertEqual(self.factorial(i), i * self.factorial(i - 1))

  def test_bad_faculty(self, ) -> None:
    """
    This method provides tests for the 'factorial' method of the
    'CombinatoricsTest' class, testing that it raises a ValueError for
    negative input.
    """

    with self.assertRaises(ValueError):
      self.factorial(-1)
