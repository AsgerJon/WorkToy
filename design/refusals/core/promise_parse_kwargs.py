"""
RefusedParseKwargs holds the refusals that belong with
'design.promises.core.promise_parse_kwargs'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.waitaminute import TypeException


class RefusedParseKwargs(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A value of no accepted type raises 'TypeException'. Source:
  the 'parseKwargs' docstring.
  """

  def test_bool_passes_as_int(self) -> None:
    value, _ = Object.parseKwargs('count', int, count=True)
    with self.assertRaises(Exception) as refused:
      Object.parseKwargs('flag', bool, flag=1)
    self.assertIsInstance(refused.exception, TypeException)

  def test_wrong_type(self) -> None:
    with self.assertRaises(Exception) as refused:
      Object.parseKwargs('scale', float, scale='2')
    self.assertIsInstance(refused.exception, TypeException)
