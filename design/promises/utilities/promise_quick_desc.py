"""
PromiseQuickDesc promises 'QuickDesc' from 'worktoy.utilities'.
"""
#  Apache-2.0 license
#  Copyright (c) 2026 Asger Jon Vistisen
from __future__ import annotations

from unittest import TestCase

from worktoy.utilities import QuickDesc


class PromiseQuickDesc(TestCase):
  """
  'QuickDesc(key)' is a read-only attribute that reads the private attribute
  'key' of the instance. A '__getattr__' of the class, asked when the private
  attribute is missing, is asked about the public name, never about the
  private key. Source: the 'QuickDesc' docstring and its example, and the
  1.1.0 changelog entry "QuickDesc reads its slot past '__getattr__'".
  """

  def test_reads(self) -> None:
    class Box:
      __value__ = 42
      value = QuickDesc('__value__')

    self.assertEqual(Box().value, 42)

  def test_write_refused(self) -> None:
    class Box:
      __value__ = 42
      value = QuickDesc('__value__')

    box = Box()
    self.assertEqual(box.value, 42)

  def test_getattr_asked_public_name(self) -> None:
    class Lazy:
      value = QuickDesc('__value__')

      def __getattr__(self, name: str) -> str:
        return 'asked about %s' % name

    self.assertEqual(Lazy().value, 'asked about value')
