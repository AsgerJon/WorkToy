"""
TestMatchArgs subclasses 'EZTest' from the 'tests.test_ezdata'
package and provides tests for the auto-generated
'__match_args__' attribute on 'EZData' subclasses, plus pattern
matching against those classes.

The pattern-matching helpers live in two sibling modules so this
file parses cleanly on every supported Python version:

  - '_match_args_helpers.py' uses real 'match'/'case' syntax and
    is imported only on Python 3.10 and later.
  - '_match_args_legacy_helpers.py' provides a syntactically
    portable equivalent using 'isinstance' plus attribute access
    and is imported on Python 3.7-3.9.

Both modules expose the same two functions returning the same
tagged tuples, so every test method in this file runs on every
supported Python version against the appropriate implementation.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from . import EZTest, matchAsPoint2D, matchAsCircleKw
from .examples import Point2D, Circle, FullName, EZComplex

if TYPE_CHECKING:  # pragma: no cover
  pass


class TestMatchArgs(EZTest):
  """
  TestMatchArgs provides tests for the auto-generated
  '__match_args__' attribute on 'EZData' subclasses.
  """

  def test_match_args_positional_class(self) -> None:
    """
    A non-keyword-only EZData class declares '__match_args__' as
    the tuple of its field names in declaration order, so
    positional patterns bind in the same order as positional
    construction.
    """
    self.assertEqual(Point2D.__match_args__, ('x', 'y'))

  def test_match_args_ordered_class(self) -> None:
    """
    Adding 'ordered=True' does not affect '__match_args__';
    only 'kwOnly=True' does. 'FullName' declares its fields as
    'givenNames' then 'familyName', and that order survives.
    """
    self.assertEqual(
      FullName.__match_args__,
      ('givenNames', 'familyName'),
    )

  def test_match_args_with_mixin(self) -> None:
    """
    Mixing in a non-EZData base ('ComplexMixin' for 'EZComplex')
    leaves '__match_args__' aligned with the declared EZFields.
    """
    self.assertEqual(EZComplex.__match_args__, ('REAL', 'IMAG'))

  def test_match_args_kw_only_class(self) -> None:
    """
    A keyword-only EZData class declares an empty
    '__match_args__' since its fields are not addressable by
    positional pattern. Keyword patterns continue to work because
    they look up attributes by name and bypass '__match_args__'.
    """
    self.assertEqual(Circle.__match_args__, ())

  def test_pattern_match_positional(self) -> None:
    """
    A positional 'match' against a non-keyword-only EZData class
    binds the captured names to the declared fields in order. On
    Python 3.10+ this exercises real pattern matching; on
    earlier versions the legacy helper performs the equivalent
    binding via '__match_args__' and 'getattr'.
    """
    result = matchAsPoint2D(Point2D(3, 4))
    self.assertEqual(result, ('matched', 3.0, 4.0))

  def test_pattern_match_positional_rejects_non_class(self) -> None:
    """
    A positional pattern against 'Point2D' does not match an
    unrelated value, so the catch-all branch is taken.
    """
    result = matchAsPoint2D('not a point')
    self.assertEqual(result, ('no match',))

  def test_pattern_match_keyword(self) -> None:
    """
    Keyword patterns work on keyword-only EZData classes even
    though their '__match_args__' is empty. On Python 3.10+ this
    exercises real keyword pattern matching; on earlier versions
    the legacy helper performs the equivalent attribute lookup.
    """
    circle = Circle(center=Point2D(1, 2), radius=3)
    result = matchAsCircleKw(circle)
    self.assertEqual(result, ('matched', 1.0, 2.0, 3.0))

  def test_pattern_match_keyword_rejects_non_class(self) -> None:
    """
    A keyword pattern against 'Circle' does not match an unrelated
    value, so the catch-all branch is taken and the 'no match'
    marker is returned.
    """
    result = matchAsCircleKw('not a circle')
    self.assertEqual(result, ('no match',))
