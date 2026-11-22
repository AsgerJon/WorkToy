"""
RefusedGenerators holds the refusals that belong with
'design.promises.lorem_ipsum.promise_generators'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.lorem_ipsum import Clause


class RefusedGenerators(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A negative count raises 'ValueError', and so does a clause too
  short for any word; a keyword other than 'charCount' raises 'TypeError'.
  Source: the docstrings of 'BaseGenerator', 'Clause', 'Sentence' and
  'Paragraph'.
  """

  def test_refusals_1(self) -> None:
    with self.assertRaises(Exception) as refused:
      Clause(-1)
    self.assertIsInstance(refused.exception, ValueError)

  def test_refusals_2(self) -> None:
    with self.assertRaises(Exception) as refused:
      str(Clause(1))
    self.assertIsInstance(refused.exception, ValueError)

  def test_refusals_3(self) -> None:
    with self.assertRaises(Exception) as refused:
      Clause(size=30)
    self.assertIsInstance(refused.exception, TypeError)
