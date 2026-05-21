"""
Pattern-matching helpers for 'TestMatchArgs'. This module uses
match / case syntax and is therefore only importable on Python
3.10 and later. The 'test_match_args.py' module imports it behind
a 'sys.version_info' guard, so on Python 3.7-3.9 this file is
never parsed; the legacy module '_match_args_legacy_helpers.py'
provides a syntactically-portable equivalent for that case.
"""
#  AGPL-3.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from typing import TYPE_CHECKING

from .examples import Point2D, Circle

if TYPE_CHECKING:  # pragma: no cover
  from typing import Any


# noinspection PyCompatibility
def matchAsPoint2D(p: Any) -> tuple:
  """
  Bind 'x' and 'y' from a positional pattern against 'Point2D'.
  Returns the bound capture as a tagged tuple, or a 'no match'
  marker when the value is not a 'Point2D'. The positional
  pattern consults 'Point2D.__match_args__' to discover which
  attributes to bind in which order.
  """
  match p:
    case Point2D(x, y):
      return ('matched', x, y)
    case _:
      return ('no match',)


# noinspection PyCompatibility
def matchAsCircleKw(c: Any) -> tuple:
  """
  Bind the fields of a 'Circle' using keyword patterns. Keyword
  patterns look attributes up by name and bypass
  '__match_args__', so they continue to work even when
  '__match_args__' is empty (the case for keyword-only EZData
  classes).
  """
  match c:
    case Circle(center=Point2D(x, y), radius=r):
      return ('matched', x, y, r)
    case _:
      return ('no match',)
