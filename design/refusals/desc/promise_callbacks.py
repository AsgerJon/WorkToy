"""
RefusedCallbacks holds the refusals that belong with
'design.promises.desc.promise_callbacks'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.desc import AttriBox
from worktoy.mcls import BaseObject
from worktoy.waitaminute.desc import NamelessCallback


class RefusedCallbacks(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. A lambda has no name to find and raises 'NamelessCallback'.
  Source: the 'BaseDescriptor' docstring and its example.
  """

  def test_lambda_refused(self) -> None:
    with self.assertRaises(Exception) as refused:
      class Account(BaseObject):
        balance = AttriBox[int](0)
        balance.onSet(lambda self, value: None)
    self.assertIsInstance(refused.exception, NamelessCallback)
