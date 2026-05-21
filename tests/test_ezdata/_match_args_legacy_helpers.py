"""
Legacy pattern-matching helpers for 'TestMatchArgs'. This module
provides equivalents of the 'match'/'case' helpers in
'_match_args_helpers.py', written using only syntax that parses
on Python 3.7 and later. Each function returns the same tagged
tuple shape as its modern counterpart, so the test methods in
'test_match_args.py' can call either implementation through the
same name and assert against the same expected output.

The positional helper consults '__match_args__' on the matched
class to discover attribute names, mirroring what the interpreter
does for a positional 'case Cls(a, b):' pattern. The keyword
helper looks attributes up by name and does not touch
'__match_args__', mirroring what the interpreter does for a
keyword 'case Cls(field=name):' pattern.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .examples import Point2D, Circle

if TYPE_CHECKING:
  from typing import Any


def matchAsPoint2D(p: Any) -> tuple:
  """
  Equivalent of the modern 'matchAsPoint2D'. Returns
  '('matched', x, y)' when 'p' is a 'Point2D' whose
  '__match_args__' lists at least two attribute names, and the
  'no match' marker tuple otherwise. Uses '__match_args__' so the
  test exercises the same auto-generated attribute the modern
  helper relies on.
  """
  if not isinstance(p, Point2D):
    return ('no match',)
  matchArgs = type(p).__match_args__
  if len(matchArgs) < 2:
    return ('no match',)
  x = getattr(p, matchArgs[0])
  y = getattr(p, matchArgs[1])
  return ('matched', x, y)


def matchAsCircleKw(c: Any) -> tuple:
  """
  Equivalent of the modern 'matchAsCircleKw'. Returns
  '('matched', x, y, r)' when 'c' is a 'Circle' whose 'center'
  is a 'Point2D', and the 'no match' marker tuple otherwise.
  Looks attributes up by name, exactly the way the modern
  keyword pattern does.
  """
  if not isinstance(c, Circle):
    return ('no match',)
  center = c.center
  if not isinstance(center, Point2D):
    return ('no match',)
  return ('matched', center.x, center.y, c.radius)
