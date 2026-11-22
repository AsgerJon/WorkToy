"""
RefusedQuickDesc holds the refusals that belong with
'design.promises.utilities.promise_quick_desc'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import QuickDesc
from worktoy.waitaminute.desc import ReadOnlyError, ProtectedError


class RefusedQuickDesc(TestCase):
  """
  Each of the following is refused, and the exception named is the one raised
  as of 1.2.3. Writing it raises 'ReadOnlyError' and deleting it raises
  'ProtectedError', both 'AttributeError'. Source: the 'QuickDesc' docstring
  and its example, and the 1.1.0 changelog entry "QuickDesc reads its slot
  past '__getattr__'".
  """

  def test_write_refused(self) -> None:
    class Box:
      __value__ = 42
      value = QuickDesc('__value__')

    box = Box()
    with self.assertRaises(Exception) as refused:
      box.value = 7
    self.assertIsInstance(refused.exception, ReadOnlyError)

  def test_delete_refused(self) -> None:
    class Box:
      __value__ = 42
      value = QuickDesc('__value__')

    box = Box()
    with self.assertRaises(Exception) as refused:
      del box.value
    self.assertIsInstance(refused.exception, ProtectedError)
