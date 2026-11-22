"""
RefusedObjectArguments holds the refusals that belong with
'design.promises.core.promise_object_arguments'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.core import Object
from worktoy.waitaminute import MissingVariable


class RefusedObjectArguments(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. 'getPrivateName' of a descriptor no class holds raises
  'MissingVariable'. Source: the 'Object' docstring and the docstrings of
  'getContextualSentinels', 'filterSentinels', 'hasSentinelArgs' and
  'getPrivateName'.
  """

  def test_private_name_unplaced(self) -> None:
    class Plain(Object):
      pass

    plain = Plain()
    with self.assertRaises(Exception) as refused:
      plain.getPrivateName()
    self.assertIsInstance(refused.exception, MissingVariable)
